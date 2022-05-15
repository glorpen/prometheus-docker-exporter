FROM python:3.10-alpine as base
MAINTAINER "Arkadiusz Dzięgiel <arkadiusz.dziegiel@glorpen.pl>"

COPY ./requirements.txt /
RUN pip install -r /requirements.txt --no-compile

FROM base as builder
COPY ./src /pkg/src
COPY ./setup.* ./LICENSE.txt /pkg/
RUN pip install /pkg --root /pkg-rootfs --no-compile

FROM base

COPY --from=builder /pkg-rootfs /

ENTRYPOINT ["python", "-m", "glorpen_docker_exporter"]
