FROM {{base}}
{% for file in files %}
COPY {{file}} /usr/bin
{% endfor %}
{% for iso in isos %}
COPY {{iso}} /images
{% endfor %}
RUN /usr/bin/packages-current
ENTRYPOINT test-xr-image-extract-rpms

