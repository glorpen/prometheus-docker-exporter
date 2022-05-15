from prometheus_client import Counter, Gauge

from glorpen_docker_exporter.metrics import Stat


def _cpu_time_in_seconds(nanoseconds: int):
    return nanoseconds / 1e+9


@Stat
def container_cpu_seconds_total(metric: Counter, data: dict):
    """Seconds that container was using CPU."""
    metric.inc(_cpu_time_in_seconds(data["cpu_stats"]["cpu_usage"]["total_usage"]))


@Stat(labels=['cpu'])
def container_cpu_percpu_seconds_total(metric: Counter, data: dict, labels: dict):
    """Seconds that container was using on each CPU."""
    for i, usage in enumerate(data["cpu_stats"]["cpu_usage"]["percpu_usage"]):
        metric.labels(cpu=i, **labels).inc(_cpu_time_in_seconds(usage))


@Stat
def container_cpu_kernel_seconds_total(metric: Counter, data: dict):
    """Seconds that container was using CPU in kernel mode."""
    metric.inc(_cpu_time_in_seconds(data["cpu_stats"]["cpu_usage"]["usage_in_kernelmode"]))


@Stat
def container_cpu_user_seconds_total(metric: Counter, data: dict):
    """Seconds that container was using CPU in user mode."""
    metric.inc(_cpu_time_in_seconds(data["cpu_stats"]["cpu_usage"]["usage_in_usermode"]))


@Stat
def container_cpu_system_seconds_total(metric: Counter, data: dict):
    """Seconds that host CPU was used."""
    metric.inc(_cpu_time_in_seconds(data["cpu_stats"]["system_cpu_usage"]))


@Stat
def container_cpu_throttled_periods_count(metric: Counter, data: dict):
    """Number of CPU throttling enforcements for a container"""
    metric.inc(data["cpu_stats"]['throttling_data']["throttled_periods"])


@Stat
def container_cpu_throttled_periods_seconds(metric: Counter, data: dict):
    """Total time that a container's CPU usage was throttled"""
    metric.inc(_cpu_time_in_seconds(data["cpu_stats"]['throttling_data']["throttled_time"]))


@Stat
def container_cpu_online(metric: Gauge, data: dict):
    """Number of available CPUs."""
    metric.inc(data["cpu_stats"]["online_cpus"])
