"""
Get remote data sources and parse their contents
"""

import feedparser
import re
import photo
import datetime
import time


class RSS(object):
    def __init__(self, url):
        self.url = url
        self.parse_feed()
        self.parse_entries()

    def parse_feed(self):
        self.feed = feedparser.parse(self.url)
        return self

    def parse_entries(self):
        self.photos = []
        rss_entries = [RSS_Entry(entry) for entry in self.get_entries()]
        for entry in rss_entries:
            images = photo.find_in_html(entry.get_content())
            photos = [photo.Photo(image, entry.data) for image in images]
            self.photos.extend(photos)

        return self

    def get_entries(self):
        return self.feed.entries if 'entries' in self.feed else {}


class RSS_Entry(object):
    def __init__(self, entry):
        self.entry = entry
        self.parse()

    def parse(self):
        entry = self.entry
        self.data = {
            'title': entry.get('title', ''),
            'author': entry.get('author', ''),
            'link': entry.get('link', ''),
            'timestamp': self.get_publish_timestamp()
        }

    def get_content(self):
        entry = self.entry
        if 'content' in entry:
            return entry.get('content')[0].get('value')
        elif 'summary' in entry:
            return entry.get('summary')
        else:
            return ''

    def get_publish_timestamp(self):
        format = "%a, %d %b %Y %H:%M:%S"
        published = self.trim_date(self.entry.get('published', ''))
        struct = datetime.datetime.strptime(published, format).timetuple()
        return time.mktime(struct)

    def trim_date(self, date):
        return re.sub(' \+[0-9]{4}$', '', date)


class WordPress(RSS):
    def __init__(self, url):
        feed_url = self.get_feed_url(url)
        super(WordPress, self).__init__(feed_url)

    def get_feed_url(self, url):
        if re.search('feed/?$', url):
            return url
        else:
            return '%s/feed' % url.rstrip('/')


class Instagram(RSS):
    def __init__(self, user):
        feed_url = self.get_feed_url(user)
        super(Instagram, self).__init__(feed_url)

    def get_feed_url(self, user):
        return 'http://widget.stagram.com/rss/n/%s/' % user
