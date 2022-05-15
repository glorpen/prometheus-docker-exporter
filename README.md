# Prometheus Docker Exporter

Exports stats from Docker API (`/containers/<id>/stat` endpoint).

Metrics are collected on each request, everything in single thread.
Fetching stats from Docker API for lots of containers on a small machine could take few seconds,
but this implementation will not use host CPU excessively (looking at you, cAdvisor!).

## Supported metrics

- cpu
- block i/o (cgroups v2)
- memory
- network

## Usage

```
usage: glorpen-docker-exporter [-h] [-a ADDR] [-p PORT] [--sysfs SYSFS]

options:
  -h, --help            show this help message and exit
  -a ADDR, --addr ADDR  address to lsiten on, defaults to 0.0.0.0
  -p PORT, --port PORT  port to listen on, defaults to 8080
  --sysfs SYSFS, -s SYSFS
                        path to sysfs to use, defaults to /sys
```

Access to `/sys` is needed for resolving block device names (`/sys/dev/block`).

Exporter needs r/w access to Docker socket (eg. `/run/docker.sock`).

Supported Docker envs:

- `DOCKER_HOST`: The URL to the Docker host.
- `DOCKER_TLS_VERIFY`: Verify the host against a CA certificate.
- `DOCKER_CERT_PATH`: A path to a directory containing TLS certificates to use when connecting to the Docker host.

### Docker

```shell
docker run -v /sys:/sys:ro -v /run/docker.sock:/run/docker.sock:rw glorpen/prometheus-docker-exporter:1.0.0
```

### Pypi

```shell
pip install glorpen-docker-exporter
python -m glorpen-docker-exporter
```

## Example Prometheus queries

CPU usage per container (as in `docker stat` command):

```
delta(container_cpu_seconds_total[2m]) / delta(container_cpu_system_seconds_total[2m]) * avg_over_time(container_cpu_online[2m])
```

Container HDD reads and writes:

```
rate(container_blkio_reads_bytes_total[2m]) > 0
rate(container_blkio_writes_bytes_total[2m]) > 0
```
