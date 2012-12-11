"""
Recommend photos to use for postagrams
"""

import time


class Recommendation(object):
    def __init__(self, photos, args={}):
        self.photos = photos
        self.parse_args(args)
        self.recommend()

    def parse_args(self, args):
        self.validation = {
            'days': args.get('validate_days', 7),
            'size': args.get('validate_size', None)
        }
        return self

    def recommend(self):
        self.recommendations = []
        for photo in self.photos:
            self.recommendations.append(photo) if self.validate(photo) else None

        return self

    def validate(self, photo):
        validated = {}

        if self.validation.get('days') <= 0:
            validated['date'] = True
        else:
            threshold = 60 * 60 * 24 * self.validation.get('days')
            validated['date'] = photo.data.get('timestamp') > int(time.time()) - threshold

        validated['photo'] = photo.validate(self.validation.get('size'))

        return all(False != validated.get(attr) for attr in validated)

    def get(self):
        return self.recommendations
