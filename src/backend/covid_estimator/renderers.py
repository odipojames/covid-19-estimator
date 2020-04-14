from rest_framework import renderers
import sys
import json


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = "text/plain"
    format = "txt"
    charset = "iso-8859-1"

    def render(self, data, media_type=None, renderer_context=None):
        data = json.dumps(data)
        return data.encode(self.charset)
