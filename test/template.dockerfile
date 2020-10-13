FROM {{base}}
{% for file in files %}
COPY {{file}} /usr/bin
{% endfor %}
CMD echo lots of weasels

