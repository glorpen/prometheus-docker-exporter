from prometheus_client import Counter

from glorpen_docker_exporter.metrics import Stat


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
