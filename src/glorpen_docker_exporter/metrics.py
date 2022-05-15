import itertools
import typing

from docker.models.containers import Container
from prometheus_client import Counter, Gauge

T = typing.TypeVar('T')


class Stat:
    _f: typing.Callable
    metric_class: typing.Type[T]

    def __init__(self, f=None, labels: list = None):
        super(Stat, self).__init__()

        self.labels = labels or []

        if f is not None:
            self(f)

    def __call__(self, f):
        self._f = f
        self._metric_class = typing.get_type_hints(f)['metric']
        return self

    @property
    def description(self):
        return self._f.__doc__

    @property
    def name(self):
        return self._f.__name__

    def update(self, metric: T, data: dict, labels: dict):
        if self.labels:
            self._f(metric=metric, labels=labels, data=data)
        else:
            self._f(metric=metric.labels(**labels), data=data)

    def metric(self, labels: list):
        return self.metric_class(self.name, self.description, self.labels + labels)


@Stat
def container_cpu_total_usage(metric: Counter, data: dict):
    """Container CPU total usage"""
    metric.inc(data["cpu_stats"]["system_cpu_usage"])


@Stat(labels=['cpu'])
def container_cpu_usage(metric: Counter, data: dict, labels: dict):
    """Container CPU percpu usage"""
    for i, usage in enumerate(data["cpu_stats"]["cpu_usage"]["percpu_usage"]):
        metric.labels(cpu=i, **labels).inc(usage)


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


@Stat
def container_cpu_kernel_total_usage(metric: Counter, data: dict):
    """Ticks that CPU spends in kernel mode"""
    metric.inc(data["cpu_stats"]["cpu_usage"]["usage_in_kernelmode"])


@Stat
def container_cpu_user_total_usage(metric: Counter, data: dict):
    """Ticks that CPU spends in user mode"""
    metric.inc(data["cpu_stats"]["cpu_usage"]["total_usage"])


@Stat
def container_cpu_system_total_usage(metric: Counter, data: dict):
    """Ticks that CPU is executing system calls on behalf of processes"""
    metric.inc(data["cpu_stats"]["system_cpu_usage"])


@Stat
def container_cpu_throttled_periods_count(metric: Counter, data: dict):
    """Number of CPU throttling enforcements for a container"""
    metric.inc(data["cpu_stats"]['throttling_data']["throttled_periods"])


@Stat
def container_cpu_throttled_periods_seconds(metric: Counter, data: dict):
    """Total time that a container's CPU usage was throttled"""
    metric.inc(data["cpu_stats"]['throttling_data']["throttled_time"])


class DeviceNameFinder:
    def __init__(self):
        super(DeviceNameFinder, self).__init__()
        self._device_cache: typing.Dict[str, str] = {}

    def find(self, major: int, minor: int):
        key = f"{major}:{minor}"
        if key in self._device_cache:
            return self._device_cache[key]

        with open(f"/sys/dev/block/{major}:{minor}/uevent", "rt") as f:
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
            ret = {
                "device": self._device_finder.find(item["major"], item["minor"])
            }
            ret.update(item)
            yield ret


@Stat(labels=["device"])
def container_blkio_reads_bytes_total(metric: Counter, labels: dict, data: BlkioStats):
    """Total bytes read by the container from device"""
    for item in data.iter("io_service_bytes_recursive", "read"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_writes_bytes_total(metric: Counter, labels: dict, data: BlkioStats):
    """Bytes written by the container"""
    for item in data.iter("io_service_bytes_recursive", "write"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_async_bytes_total(metric: Counter, labels: dict, data: BlkioStats):
    """"""
    for item in data.iter("io_service_bytes_recursive", "async"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_sync_bytes_total(metric: Counter, labels: dict, data: BlkioStats):
    """"""
    for item in data.iter("io_service_bytes_recursive", "sync"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_discard_bytes_total(metric: Counter, labels: dict, data: BlkioStats):
    """"""
    for item in data.iter("io_service_bytes_recursive", "discard"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_reads_total(metric: Counter, labels: dict, data: BlkioStats):
    """Count of read operations performed, regardless of size"""
    for item in data.iter("io_serviced_recursive", "read"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_writes_total(metric: Counter, labels: dict, data: BlkioStats):
    """Count of write operations performed, regardless of size"""
    for item in data.iter("io_serviced_recursive", "write"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_async_total(metric: Counter, labels: dict, data: BlkioStats):
    """"""
    for item in data.iter("io_serviced_recursive", "async"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_sync_total(metric: Counter, labels: dict, data: BlkioStats):
    """"""
    for item in data.iter("io_serviced_recursive", "sync"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat(labels=["device"])
def container_blkio_discard_total(metric: Counter, labels: dict, data: BlkioStats):
    """"""
    for item in data.iter("io_serviced_recursive", "discard"):
        metric.labels(device=item["device"], **labels).inc(item["value"])


@Stat
def container_mem_max_usage_bytes(metric: Counter, data: dict):
    """Container max memory usage recorded"""
    metric.inc(data["memory_stats"]["max_usage"])
