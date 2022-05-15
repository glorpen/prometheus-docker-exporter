import itertools
import typing

from prometheus_client import Counter

from glorpen_docker_exporter.metrics import Stat


class DeviceNameFinder:
    def __init__(self, sysfs_path: str):
        super(DeviceNameFinder, self).__init__()
        self._device_cache: typing.Dict[str, str] = {}
        self._sysfs_path = sysfs_path

    def find(self, major: int, minor: int):
        key = f"{major}:{minor}"
        if key in self._device_cache:
            return self._device_cache[key]

        with open(f"{self._sysfs_path}/dev/block/{major}:{minor}/uevent", "rt") as f:
            data = f.read()

        for line in data.splitlines(keepends=False):
            if line.startswith("DEVNAME="):
                self._device_cache[key] = line[8:]
                return self._device_cache[key]

        raise Exception(f"Device name not found for {major}:{minor}")

    def clear(self):
        self._device_cache.clear()


class BlkioStats:
    def __init__(self, device_finder: DeviceNameFinder, stats: dict):
        super(BlkioStats, self).__init__()
        self._device_finder = device_finder
        self._stats = {}

        for name, blkio_stats in stats["blkio_stats"].items():
            self._stats[name] = dict(
                (operation.lower(), list(items)) for operation, items in
                itertools.groupby(blkio_stats, key=lambda x: x["op"])
            )

    def iter(self, group: str, op: str):
        for item in self._stats.get(group, {}).get(op.lower(), []):
            ret = {"device": self._device_finder.find(item["major"], item["minor"])}
            ret.update(item)
            yield ret


@Stat(labels=["device"])
def container_blkio_reads_bytes_total(metric: Counter, labels: dict, data: BlkioStats):
    """Bytes read."""
    for item in data.iter("io_service_bytes_recursive", "read"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_writes_bytes_total(metric: Counter, labels: dict, data: BlkioStats):
    """Bytes written."""
    for item in data.iter("io_service_bytes_recursive", "write"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_async_bytes_total(metric: Counter, labels: dict, data: BlkioStats):
    """Bytes asynced."""
    for item in data.iter("io_service_bytes_recursive", "async"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_sync_bytes_total(metric: Counter, labels: dict, data: BlkioStats):
    """Bytes synced."""
    for item in data.iter("io_service_bytes_recursive", "sync"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_discard_bytes_total(metric: Counter, labels: dict, data: BlkioStats):
    """Bytes discarded."""
    for item in data.iter("io_service_bytes_recursive", "discard"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_reads_total(metric: Counter, labels: dict, data: BlkioStats):
    """Count of read operations performed, regardless of size."""
    for item in data.iter("io_serviced_recursive", "read"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_writes_total(metric: Counter, labels: dict, data: BlkioStats):
    """Count of write operations performed, regardless of size."""
    for item in data.iter("io_serviced_recursive", "write"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_async_total(metric: Counter, labels: dict, data: BlkioStats):
    """Count of async operations performed, regardless of size"""
    for item in data.iter("io_serviced_recursive", "async"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_sync_total(metric: Counter, labels: dict, data: BlkioStats):
    """Count of sync operations performed, regardless of size"""
    for item in data.iter("io_serviced_recursive", "sync"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_discard_total(metric: Counter, labels: dict, data: BlkioStats):
    """Count of discard operations performed, regardless of size"""
    for item in data.iter("io_serviced_recursive", "discard"):
        metric.labels(device=item["device"], **labels).inc(item["value"])
