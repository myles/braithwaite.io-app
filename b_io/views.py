# -*- coding: utf-8 -*-
from pathlib import Path

from flask import Blueprint, abort, current_app, render_template, Response

from feedgenerator import Atom1Feed
from jsonfeed import JSONFeed

from .models import Notebook, all_notebooks

blueprint = Blueprint('views', __name__)


@blueprint.route('/')
def index():
    notebook_list = all_notebooks()

    return render_template('index.html', notebooks=notebook_list)


@blueprint.route('/feed.<string:feed_type>')
def feed(feed_type):
    if feed_type not in ['json', 'xml']:
        abort(404)

    author_info = {
        'author_name': 'Myles Braithwaite',
        'author_link': 'https://mylesb.ca/',
        'author_email': 'me@mylesbraithwaite.org',
    }

    meta_info = {
        'title': 'Braithwaite I/O',
        'link': 'https://braithwaite.io/',
        'feed_guid': 'https://braithwaite.io/',
        'description': "Myles Braithwaite's Fancy Jupyter Notebooks Blog.",
        'language': 'en'
    }

    if feed_type == 'json':
        feed = JSONFeed(**{**meta_info, **author_info})
        mimetype = feed.content_type
    else:
        feed = Atom1Feed(**meta_info)
        mimetype = 'application/atom+xml'

    for notebook in all_notebooks():
        feed.add_item(
            guid='https://braithwaite.io{}'.format(notebook.url),
            title=notebook.name,
            link='https://braithwaite.io{}'.format(notebook.url),
            summary=notebook.summary,
            description=notebook.content,
            pubdate=notebook.published,
            categories=notebook.category,
            **author_info
        )

    return Response(feed.writeString('utf-8'), mimetype=mimetype)


@blueprint.route('/<slug>/')
def notebook(slug):
    content_path = Path(current_app.config['CONTENT_ROOT'])

    try:
        notebook = Notebook(content_path.joinpath(slug))

        return render_template('notebook.html', notebook=notebook)
    except IOError:
        abort(404)


@blueprint.route('/<slug>/notebook.ipynb')
def jupyter_notebook(slug):
    content_path = Path(current_app.config['CONTENT_ROOT'])

    notebook_path = content_path.joinpath(slug, 'notebook.ipynb')

    try:
        with open(notebook_path) as fobj:
            return Response(fobj.read(), mimetype='application/vnd.jupyter')
    except IOError:
        abort(404)
