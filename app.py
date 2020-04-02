from flask import Flask
from infrastructure.blog import blogmain

import datetime
import functools
import os
import re
import urllib

from flask import (Flask, abort, flash, Markup, redirect, render_template,
                   request, Response, session, url_for)
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache
from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from playhouse.sqlite_ext import *
# TODO: Move app.config to separate file

app = Flask(__name__)
app.config.from_object(__name__)

ADMIN_PASSWORD = 'blogPOSTSdonotread533!'
APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'blogstorage.db')
DEBUG = True
SECRET_KEY = '42804280'  # Used by Flask to encrypt session cookie.
SITE_WIDTH = 800


def main():
    register_blueprints()
    blogmain()
    app.run(debug=True)


def register_blueprints():
    from views import home_views, blog_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(blog_views.blueprint)


def login():
    if request.method == 'POST' and request.form.get('password'):
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            loginstate = True
            return loginstate
        else:
            flash('Incorrect password.', 'danger')
            loginstate = False
            return loginstate



@app.template_filter('clean_querystring')
def clean_querystring(request_args, *keys_to_remove, **new_values):
    querystring = dict((key, value) for key, value in request_args.items())
    for key in keys_to_remove:
        querystring.pop(key, None)
    querystring.update(new_values)
    return urllib.urlencode(querystring)

"""
@app.errorhandler(404)
def not_found(exc):
    return Response('<h3>Not found</h3>'), 404
"""

if __name__ == '__main__':
    main()
else:
    register_blueprints()
