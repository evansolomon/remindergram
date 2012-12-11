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
        self.photo_tests = {
            'days': args.get('days', 7),
            'size': args.get('size', None)
        }
        return self

    def recommend(self):
        self.recommendations = []
        for photo in self.photos:
            self.recommendations.append(photo) if self.validate(photo) else None

        return self

    def validate(self, photo):
        return Photo_Validation(photo, self.photo_tests).valid

    def get(self):
        return self.recommendations


class Photo_Validation(object):
    def __init__(self, photo, tests):
        self.photo = photo
        self.tests = tests
        self.valid = self.validate()

    def validate(self):
        results = []
        for (test, param) in self.tests.items():
            results.append(self.run(test, param))

        return not any(False == result for result in results)

    def run(self, test, param):
        callback = 'test_%s' % test
        return getattr(self, callback)(param) if self.has_test(callback) else None

    def has_test(self, test):
        return hasattr(self, test) and callable(getattr(self, test))

    def test_days(self, days):
        if days <= 0:
            return True
        else:
            threshold = 60 * 60 * 24 * days
            return self.photo.data.get('timestamp') > int(time.time()) - threshold

    def test_size(self, size):
        return self.photo.validate(size)
