from docker.models.containers import Container
from prometheus_client import Gauge

from glorpen_docker_exporter.metrics import Stat


@Stat
def container_status(metric: Gauge, data: Container):
    """Container status"""
    text = data.attrs['State'].lower()
    value = 10
    if text == "running":
        value = 0
    if text == "exited":
        value = 1

    metric.set(value)
