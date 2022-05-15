import argparse

from prometheus_client import metrics

from glorpen_docker_exporter.exporter import Exporter

# no easily configurable option in package
metrics._use_created = False

p = argparse.ArgumentParser(prog="glorpen-docker-exporter")
p.add_argument("-a", "--addr", default='0.0.0.0', help="address to lsiten on, defaults to 0.0.0.0")
p.add_argument("-p", "--port", default=8080, type=int, help="port to listen on, defaults to 8080")
p.add_argument("--sysfs", "-s", default="/sys", help="path to sysfs to use, defaults to /sys")

ns = p.parse_args()

Exporter(ns.sysfs).start_wsgi_server(addr=ns.addr, port=ns.port)
