"""
Manage photo items
"""

from BeautifulSoup import BeautifulSoup
from PIL import Image
from cStringIO import StringIO
from urlparse import urlparse
import urllib2

# Seemingly consistent ratio
BYTES_PER_PIXEL = 0.25


def find_in_html(html):
    images = BeautifulSoup(html).findAll('img')
    return [image.get('src') for image in images]


class Photo(object):
    def __init__(self, url, attrs):
        self.url = url
        self.attrs = attrs
        self.set_defaults()
        self.parse_image()

    def set_defaults(self):
        self.defaults = {
            'minimum_size': 500
        }
        self.fields = ('title', 'author', 'link', 'timestamp')

        return self

    def filter_attrs(self):
        self.data = {field: self.attrs.get(field) for field in self.fields}
        return self

    def validate(self, minimum=False):
        if any(False == self.data.get(field, False) for field in self.fields):
            return False

        minimum = minimum or self.defaults.get('minimum_size')
        return all(dimension >= minimum for dimension in self.size)

    def parse_image(self):
        self.filter_attrs()
        self.get_size()
        return self

    def get_size(self):
        bytes = self.get_bytes()
        if bytes:
            pixels = int(bytes) / BYTES_PER_PIXEL
            side = int(pixels ** 0.5)
            dimensions = (side, side)
        else:
            image_file = urllib2.urlopen(self.url).read()
            io = StringIO(image_file)
            image = Image.open(io)
            dimensions = image.size if hasattr(image, 'size') else (0, 0)

        self.size = dimensions
        return self

    def get_bytes(self):
        request = urllib2.Request(self.url)
        request.get_method = lambda: 'HEAD'
        response = urllib2.urlopen(request)
        bytes = response.info().getheader('Content-Length') or 0
        return int(bytes)

    # A couple of deduplication methods
    def __eq__(self, compare):
        return self.url == compare.url

    def __hash___(self):
        return hash(('url', self.url))
