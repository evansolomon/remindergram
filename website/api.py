from flask import jsonify, request, Response
import json
from remindergram import source, recommendation


def recommendation_photos():
    query = _Query(request)
    if not hasattr(source, query.service):
        return jsonify({'error': 'Invalid service'})

    s = getattr(source, query.service)(query.identifier)
    if not s.photos:
        return jsonify({'error': 'No photos'})

    recs = recommendation.Recommendation(s.photos, {'days': query.days, 'size': query.size})
    photos = [rec.url for rec in recs.get()]
    if not photos:
        return jsonify({'error': 'No photos'})

    return Response(json.dumps(photos), mimetype='application/json')


class _Query(object):
    def __init__(self, request):
        self.set_defaults()
        self.parse_request(request)

    def set_defaults(self):
        self.days = 20
        self.size = 500
        return self

    def parse_request(self, request):
        for key, val in request.form.items():
            setattr(self, key, val)

        return self

    # Fallback, always be able to request a query attribute without errors
    def __getattr__(self, attr):
        return None
