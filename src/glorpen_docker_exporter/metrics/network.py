from prometheus_client import Counter

from glorpen_docker_exporter.metrics import Stat


def _with_network_data(data: dict, stat_name: str):
    if "networks" in data:
        for name, stat in data["networks"].items():
            yield name, stat[stat_name]


@Stat(labels=["interface"])
def container_net_rx_bytes_total(metric: Counter, labels: dict, data: dict):
    """Total bytes received."""
    for name, stat in _with_network_data(data, "rx_bytes"):
        metric.labels(interface=name, **labels).inc(stat)


@Stat(labels=["interface"])
def container_net_tx_bytes_total(metric: Counter, labels: dict, data: dict):
    """Total bytes send."""
    for name, stat in _with_network_data(data, "tx_bytes"):
        metric.labels(interface=name, **labels).inc(stat)


@Stat(labels=["interface"])
def container_net_rx_errors_count(metric: Counter, labels: dict, data: dict):
    """Total count of received malformed frames."""
    for name, stat in _with_network_data(data, "rx_errors"):
        metric.labels(interface=name, **labels).inc(stat)


@Stat(labels=["interface"])
def container_net_tx_errors_count(metric: Counter, labels: dict, data: dict):
    """Total count of errors when sending frames."""
    for name, stat in _with_network_data(data, "tx_errors"):
        metric.labels(interface=name, **labels).inc(stat)


@Stat(labels=["interface"])
def container_net_rx_dropped_count(metric: Counter, labels: dict, data: dict):
    """Total count of dropped frames when receiving."""
    for name, stat in _with_network_data(data, "rx_dropped"):
        metric.labels(interface=name, **labels).inc(stat)


@Stat(labels=["interface"])
def container_net_tx_dropped_count(metric: Counter, labels: dict, data: dict):
    """Total count of dropped frames when sending."""
    for name, stat in _with_network_data(data, "tx_dropped"):
        metric.labels(interface=name, **labels).inc(stat)


@Stat(labels=["interface"])
def container_net_rx_packets_total(metric: Counter, labels: dict, data: dict):
    """Total packets received."""
    for name, stat in _with_network_data(data, "rx_packets"):
        metric.labels(interface=name, **labels).inc(stat)


@Stat(labels=["interface"])
def container_net_tx_packets_total(metric: Counter, labels: dict, data: dict):
    """Total packets send."""
    for name, stat in _with_network_data(data, "tx_packets"):
        metric.labels(interface=name, **labels).inc(stat)
