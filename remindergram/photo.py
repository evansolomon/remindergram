"""
Manage photo items
"""

from BeautifulSoup import BeautifulSoup
from PIL import Image
from cStringIO import StringIO
from urlparse import urlparse
import urllib2


def find_in_html(html):
    images = BeautifulSoup(html).findAll('img')
    return [image.get('src') for image in images]


class Photo(object):
    def __init__(self, file, attrs, args={}):
        self.file = self.get_file(file)
        self.attrs = attrs
        self.attr_fields = ('title', 'author', 'link', 'timestamp')
        self.set_defaults()
        self.parse()

    def get_file(self, file):
        if urlparse(file).netloc:
            file = self.get_from_url(file)

        return file

    def set_defaults(self):
        self.defaults = {
            'minimum_size': 500
        }
        return self

    def parse(self):
        self.parse_size()
        self.data = {field: self.attrs.get(field) for field in self.attr_fields}
        return self

    def validate(self, minimum=False):
        if not all(False != self.attrs.get(field, False) for field in self.attr_fields):
            return False

        minimum = minimum or self.defaults.get('minimum_size')
        return all(dimension >= minimum for dimension in self.size)

    def parse_size(self):
        image = Image.open(self.file)
        self.size = image.size if hasattr(image, 'size') else (0, 0)
        return self

    def get_from_url(self, url):
        image = urllib2.urlopen(url).read()
        return StringIO(image)
