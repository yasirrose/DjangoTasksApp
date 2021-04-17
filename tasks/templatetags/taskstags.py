from django import template
from django.templatetags.static import static
import json
from os import path

register = template.Library()


@register.simple_tag
def assetlink(filename):
    try:
        file = path.dirname(path.dirname(path.abspath(__file__)))
        assets = path.join(file, "static", "dist", "assets-manifest.json")
        with open(assets) as f:
            data = json.load(f)
            return static('dist/{}'.format(data[filename]))
    except Exception as e:
        return None
