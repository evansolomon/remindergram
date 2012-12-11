"""
Get remote data sources and parse their contents
"""

import feedparser
import re
import photo


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
        for entry in self.get_entries():
            rss_entry = RSS_Entry(entry)
            files = photo.find_in_html(rss_entry.data.get('content'))
            for file in files:
                _photo = photo.Photo(file, rss_entry.data)
                self.photos.append(_photo)

        return self

    def get_entries(self):
        return self.feed.entries if 'entries' in self.feed else {}


class RSS_Entry(object):
    def __init__(self, entry):
        self.parse(entry)

    def parse(self, entry):
        self.data = {
            'title': entry.get('title', ''),
            'content': self.get_content(entry),
            'author': entry.get('author', ''),
            'link': entry.get('link', ''),
            'date': entry.get('published', '')
        }

    def get_content(self, entry):
        if 'content' in entry:
            return entry.get('content')[0].get('value')
        elif 'summary' in entry:
            return entry.get('summary')
        else:
            return ''


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
