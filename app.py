from config import ADMIN_PASSWORD
from infrastructure.blog import blogmain
import urllib
from flask import (Flask, abort, flash, Markup, redirect, render_template,
                   request, Response, session, url_for)


app = Flask(__name__)
app.config.from_pyfile('config.py')


def main():
    register_blueprints()
    blogmain()
    app.run(debug=True)


def register_blueprints():
    from views import home_views, blog_views, capstone_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(capstone_views.blueprint)
    app.register_blueprint(blog_views.blueprint)
# TODO: Fix blog?


def login():
    if request.method == 'POST' and request.form.get('password'):
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            loginstate = True
            print('password match and returning loginstate ', loginstate)
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
