# -----------------------------------------------------------------------------
# dockerfile -- Run script in a container
#
# December 2020, Patrick Smears
#
# Copyright (c) 2020 by Cisco Systems, Inc.
# All rights reserved.
# -----------------------------------------------------------------------------
FROM {{from_}}
{% for file in files %}COPY {{file}} /usr/bin
{% endfor %}
{% for iso in isos %}COPY {{iso}} /images/{{iso}}
{% endfor %}
RUN /usr/bin/prep-{{base}}
ENTRYPOINT {{entrypoint}}

