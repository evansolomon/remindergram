try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Remindergram prompts you to send postagrams from photos you have posted around the web.',
    'author': 'Evan Solomon',
    'url': 'http://evansolomon.me',
    'download_url': 'http://github.com/evansolomon/remindergram',
    'author_email': 'evan@evanalyze.com',
    'version': '1.0',
    'scripts': [],
    'install_requires': ['feedparser', 'nose', 'BeautifulSoup', 'PIL', 'Flask', 'flask-bootstrap'],
    'packages': ['remindergram'],
    'name': 'remindergram',
    'license': 'MIT License'
}

setup(**config)
