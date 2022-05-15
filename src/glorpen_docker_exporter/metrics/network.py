from prometheus_client import Counter

from glorpen_docker_exporter.metrics import Stat


@Stat(labels=["interface"])
def container_net_rx_bytes_total(metric: Counter, labels: dict, data: dict):
    """Total bytes received."""
    for name, stat in data["networks"].items():
        metric.labels(interface=name, **labels).inc(stat["rx_bytes"])


@Stat(labels=["interface"])
def container_net_tx_bytes_total(metric: Counter, labels: dict, data: dict):
    """Total bytes send."""
    for name, stat in data["networks"].items():
        metric.labels(interface=name, **labels).inc(stat["tx_bytes"])


@Stat(labels=["interface"])
def container_net_rx_errors_count(metric: Counter, labels: dict, data: dict):
    """Total count of received malformed frames."""
    for name, stat in data["networks"].items():
        metric.labels(interface=name, **labels).inc(stat["rx_errors"])


@Stat(labels=["interface"])
def container_net_tx_errors_count(metric: Counter, labels: dict, data: dict):
    """Total count of errors when sending frames."""
    for name, stat in data["networks"].items():
        metric.labels(interface=name, **labels).inc(stat["tx_errors"])


@Stat(labels=["interface"])
def container_net_rx_dropped_count(metric: Counter, labels: dict, data: dict):
    """Total count of dropped frames when receiving."""
    for name, stat in data["networks"].items():
        metric.labels(interface=name, **labels).inc(stat["rx_dropped"])


@Stat(labels=["interface"])
def container_net_tx_dropped_count(metric: Counter, labels: dict, data: dict):
    """Total count of dropped frames when sending."""
    for name, stat in data["networks"].items():
        metric.labels(interface=name, **labels).inc(stat["tx_dropped"])


@Stat(labels=["interface"])
def container_net_rx_packets_total(metric: Counter, labels: dict, data: dict):
    """Total packets received."""
    for name, stat in data["networks"].items():
        metric.labels(interface=name, **labels).inc(stat["rx_packets"])


@Stat(labels=["interface"])
def container_net_tx_packets_total(metric: Counter, labels: dict, data: dict):
    """Total packets send."""
    for name, stat in data["networks"].items():
        metric.labels(interface=name, **labels).inc(stat["tx_packets"])
