try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A collection of screens to display on a Raspberry Pi',
    'author': 'Simon Brydon',
    'url': '',
    'download_url': '',
    'author_email': 'simonbrydon@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'urwid', 'tornado', 'requests', 'feedparser'],
    'packages': ['piscreens'],
    'scripts': [],
    'name': 'Pi Screens'
}

setup(**config)
