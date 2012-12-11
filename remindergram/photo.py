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
    def __init__(self, file, attrs):
        self.set_defaults()
        self.fields = ('title', 'author', 'link', 'timestamp')
        self.file = self.get_file(file)
        self.data = self.filter_attrs(attrs)
        self.size = self.get_size()

    def get_file(self, file):
        if urlparse(file).netloc:
            file = self.get_from_url(file)

        return file

    def set_defaults(self):
        self.defaults = {
            'minimum_size': 500
        }
        return self

    def filter_attrs(self, attrs):
        return {field: attrs.get(field) for field in self.fields}

    def validate(self, minimum=False):
        if any(False == self.data.get(field, False) for field in self.fields):
            return False

        minimum = minimum or self.defaults.get('minimum_size')
        return all(dimension >= minimum for dimension in self.size)

    def get_size(self):
        image = Image.open(self.file)
        return image.size if hasattr(image, 'size') else (0, 0)
        return self

    def get_from_url(self, url):
        image = urllib2.urlopen(url).read()
        return StringIO(image)
