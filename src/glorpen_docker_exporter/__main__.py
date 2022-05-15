from prometheus_client import metrics

from glorpen_docker_exporter.exporter import Exporter

# no easily configurable option in package
metrics._use_created = False

Exporter().start_wsgi_server(port=8080)
