FROM {{from_}}
{% for file in files %}
COPY {{file}} /usr/bin
{% endfor %}
{% for iso in isos %}
COPY {{iso}} /images/{{iso}}
{% endfor %}
RUN /usr/bin/prep-{{base}} /usr/bin/packages-{{base}}
ENTRYPOINT test-xr-image-extract-rpms

