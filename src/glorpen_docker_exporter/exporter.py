import itertools
import typing
from typing import Iterable
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

import docker
from docker.models.containers import Container
from prometheus_client import CollectorRegistry, Metric, make_wsgi_app
from prometheus_client.metrics import MetricWrapperBase

from glorpen_docker_exporter.metrics import Stat, blkio as metrics_blkio, container as metrics_container, \
    memory as metrics_memory, network as metrics_network, stats as metrics_stats
from glorpen_docker_exporter.metrics.blkio import BlkioStats, DeviceNameFinder


class OnDemandCollectorRegistry(CollectorRegistry):
    def on_collect(self):
        pass

    def collect(self) -> Iterable[Metric]:
        self.on_collect()
        yield from super(OnDemandCollectorRegistry, self).collect()


class SilentHandler(WSGIRequestHandler):
    def log_message(self, *args):
        pass


def iter_stats(*mods):
    for mod in mods:
        for name in dir(mod):
            v = getattr(mod, name)
            if isinstance(v, Stat):
                yield v


class Exporter:
    def __init__(self, sysfs_path: str = "/sys"):
        super(Exporter, self).__init__()

        self.registry = OnDemandCollectorRegistry(auto_describe=True)
        self.registry.on_collect = self.update
        self.client = docker.from_env()

        self._registered_metrics: typing.Dict[Stat, MetricWrapperBase] = {}

        self._container_metrics = list(iter_stats(metrics_container))
        self._stats_metrics = list(iter_stats(metrics_stats, metrics_memory, metrics_network))
        self._blkio_metrics = list(iter_stats(metrics_blkio))

        self._device_finder = DeviceNameFinder(sysfs_path)

        self._container_labels = ['name', 'image', 'id', 'image_id']

        self._register_metrics(
            self._container_metrics,
            self._stats_metrics,
            self._blkio_metrics
        )

    def _register_metrics(self, *items):
        for stat in itertools.chain(*items):
            metric = stat.metric(self._container_labels)
            self._registered_metrics[stat] = metric
            self.registry.register(metric)

    def _clear(self):
        for metric in self._registered_metrics.values():
            metric.clear()
        self._device_finder.clear()

    def update(self):
        self._clear()

        c: Container
        for c in self.client.containers.list(sparse=True):
            name = c.name or c.attrs["Names"][0].lstrip("/")
            image_id = c.attrs.get('ImageID')
            image = c.attrs['Image']
            container_labels = {"id": c.id, "name": name, "image_id": image_id, "image": image}

            for stat in self._container_metrics:
                stat.update(metric=self._registered_metrics[stat], labels=container_labels, data=c)

            stats = self.client.api.get(
                f"{self.client.api.base_url}/containers/{c.id}/stats?stream=false&one-shot=true"
            ).json()

            for stat in self._stats_metrics:
                stat.update(metric=self._registered_metrics[stat], labels=container_labels, data=stats)

            blkio_data = BlkioStats(self._device_finder, stats)
            for stat in self._blkio_metrics:
                stat.update(metric=self._registered_metrics[stat], labels=container_labels, data=blkio_data)

    def start_wsgi_server(self, port: int, addr: str = '0.0.0.0') -> None:
        app = make_wsgi_app(self.registry)
        httpd = make_server(addr, port, app, WSGIServer, handler_class=SilentHandler)
        httpd.serve_forever()
