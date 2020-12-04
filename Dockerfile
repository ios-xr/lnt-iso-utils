# -----------------------------------------------------------------------------
# dockerfile -- Run script in a container
#
# December 2020, Patrick Smears
#
# Copyright (c) 2020 by Cisco Systems, Inc.
# All rights reserved.
# -----------------------------------------------------------------------------
FROM debian:9.13-slim
COPY xr-image-extract-rpms /usr/bin
COPY setup/prep-debian /usr/bin


RUN /usr/bin/prep-debian
ENTRYPOINT /bin/bash
