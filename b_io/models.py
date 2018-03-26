import datetime
import re
from pathlib import Path

import toml
import nbformat
from nbconvert import HTMLExporter

from flask import current_app, url_for

re_folder = re.compile(r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-'
                       r'(?P<slug>[-\w]+)$')


class Notebook(object):
    """Braithwaite I/O Notebook Entry."""

    def __init__(self, path):
        self.path = Path(path)

        meta_path = self.path.joinpath('meta.toml')

        if meta_path.is_file():
            with open(meta_path) as fobj:
                self.__meta = toml.loads(fobj.read())
        else:
            self.__meta = {}

        notebook_path = self.path.joinpath('notebook.ipynb')

        with open(notebook_path) as fobj:
            notebook = nbformat.reads(fobj.read(), as_version=4)

        html_exporter = HTMLExporter()
        html_exporter.template_file = 'basic'

        (self.__body, self.__resources) = \
            html_exporter.from_notebook_node(notebook)

    @property
    def name(self):
        if self.__meta.get('name'):
            return self.__meta.get('name')
        else:
            match = re_folder.match(self.path.name).groupdict()
            return match['slug'].replace('-', ' ')

    @property
    def published(self):
        if self.__meta.get('published'):
            return self.__meta.get('published')
        else:
            match = re_folder.match(self.path.name).groupdict()
            return datetime.datetime.strptime(
                '{year}-{month}-{day}'.format(match),
                '%Y-%m-%d')

    @property
    def updated(self):
        if self.__meta.get('updated'):
            return self.__meta.get('updated')
        else:
            match = re_folder.match(self.path.name).groupdict()
            return datetime.datetime.strptime(
                '{year}-{month}-{day}'.format(match),
                '%Y-%m-%d')

    @property
    def hidden(self):
        return self.__meta.get('hidden', False)

    @property
    def category(self):
        return self.__meta.get('category')

    @property
    def summary(self):
        return self.__meta.get('summary')

    @property
    def content(self):
        return self.__body

    @property
    def slug(self):
        return self.path.name

    @property
    def url(self):
        return url_for('views.notebook', slug=self.slug)

    @property
    def notebook_url(self):
        return url_for('views.jupyter_notebook', slug=self.slug)

    @property
    def resources(self):
        self.__resources


def all_notebooks():
    def gen():
        content_path = Path(current_app.config['CONTENT_ROOT'])

        notebooks = content_path.glob('**/meta.toml')

        for path in notebooks:
            yield Notebook(path.parent)

    g = list(gen())
    g.sort(key=lambda x: x.published, reverse=True)

    return g
