from flask import jsonify, request, Response
import json
from remindergram import source, recommendation


def get_photos():
    service = request.form['service']
    identifier = request.form['identifier']
    if not hasattr(source, service):
        return jsonify({'error': 'Invalid service'})

    s = getattr(source, service)(identifier)
    if not s.photos:
        return jsonify({'error': 'No photos'})

    recs = recommendation.Recommendation(s.photos, {'days': 20, 'size': 500})
    photos = [rec.url for rec in recs.get()]
    if not len(photos):
        return jsonify({'error': 'No photos'})

    return Response(json.dumps(photos), mimetype='application/json')
