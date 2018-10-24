import datetime
import json
import re
from pathlib import Path

import toml
import nbformat
from dateutil.parser import parse as dt_parse
from nbconvert import HTMLExporter

from flask import current_app, url_for

RE_FOLDER = re.compile(
    r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-" r"(?P<slug>[-\w]+)$"
)


class Mention(object):
    """Braithwaite I/O Mention Entry."""

    @classmethod
    def parse(cls, path):
        """Parse the mention."""
        with open(path) as fobj:
            data = json.loads(fobj.read())

        mention = cls()
        setattr(mention, "_json", data)

        for k, v in data.items():
            if k == "verified_date":
                setattr(mention, k, dt_parse(v))
            else:
                setattr(mention, k, v)

        return mention


class Notebook(object):
    """Braithwaite I/O Notebook Entry."""

    def __init__(self, path):
        self.path = Path(path)
        self.mention_path = self.path.joinpath("_mentions")

        meta_path = self.path.joinpath("meta.toml")

        if meta_path.is_file():
            with open(meta_path) as fobj:
                self.__meta = toml.loads(fobj.read())
        else:
            self.__meta = {}

        notebook_path = self.path.joinpath("notebook.ipynb")

        with open(notebook_path) as fobj:
            notebook = nbformat.reads(fobj.read(), as_version=4)

        html_exporter = HTMLExporter(
            template_path=[str(current_app.config["TEMPLATES_FOLDER"])]
        )
        html_exporter.template_file = "nbconvert"

        (self.__body, self.__resources) = html_exporter.from_notebook_node(
            notebook
        )

    @property
    def name(self):
        if self.__meta.get("name"):
            return self.__meta.get("name")
        else:
            match = RE_FOLDER.match(self.path.name).groupdict()
            return match["slug"].replace("-", " ")

    @property
    def published(self):
        if self.__meta.get("published"):
            return self.__meta.get("published")
        else:
            match = RE_FOLDER.match(self.path.name).groupdict()
            return datetime.datetime.strptime(
                "{year}-{month}-{day}".format(match), "%Y-%m-%d"
            )

    @property
    def updated(self):
        if self.__meta.get("updated"):
            return self.__meta.get("updated")

        match = RE_FOLDER.match(self.path.name).groupdict()

        return datetime.datetime.strptime(
            "{year}-{month}-{day}".format(**match), "%Y-%m-%d"
        )

    @property
    def hidden(self):
        return self.__meta.get("hidden", False)

    @property
    def category(self):
        return self.__meta.get("category")

    @property
    def summary(self):
        return self.__meta.get("summary")

    @property
    def content(self):
        return self.__body

    @property
    def slug(self):
        return self.path.name

    @property
    def url(self):
        return url_for("views.notebook", slug=self.slug)

    @property
    def notebook_url(self):
        return url_for("views.jupyter_notebook", slug=self.slug)

    @property
    def resources(self):
        return self.__resources

    def list_mentions(self):
        file_list = self.mention_path.glob("*.json")

        mentions = [Mention.parse(file_name) for file_name in file_list]

        mentions.sort(key=lambda x: x.verified_date, reverse=True)

        return mentions


def all_notebooks():
    def gen():
        content_path = Path(current_app.config["CONTENT_ROOT"])

        notebooks = content_path.glob("**/meta.toml")

        for path in notebooks:
            yield Notebook(path.parent)

    g = list(gen())
    g.sort(key=lambda x: x.published, reverse=True)

    return g


def all_mentions():
    def gen():
        content_path = Path(current_app.config["CONTENT_ROOT"])

        mentions = content_path.glob("**/_mentions/*.json")

        for mention in mentions:
            yield Mention(mention)

    g = list(gen())
    g.sort(key=lambda x: x.id, reversed=True)

    return g
