from flask import Flask, render_template, jsonify, request, Response
import json
from flask.ext.bootstrap import Bootstrap
from remindergram import source, recommendation

app = Flask(__name__)
Bootstrap(app)

app.config['BOOTSTRAP_USE_MINIFIED'] = True
app.config['BOOTSTRAP_USE_CDN'] = True
app.config['BOOTSTRAP_FONTAWESOME'] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get/photos', methods=['POST'])
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
