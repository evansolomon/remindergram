from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
import api

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
    return api.get_photos()
