FROM debian:9.13-slim
COPY xr-image-extract-rpms /usr/bin
COPY setup/prep-debian /usr/bin
COPY setup/packages-debian /usr/bin


RUN /usr/bin/prep-debian /usr/bin/packages-debian
ENTRYPOINT /bin/bash
