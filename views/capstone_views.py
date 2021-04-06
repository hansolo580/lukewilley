import flask
import functools

#from app import login
from infrastructure.view_modifiers import response

from flask import (session, redirect, url_for, render_template, request)

blueprint = flask.Blueprint('capstone', __name__, template_folder='templates')


"""@blueprint.route('/login/', methods=['GET', 'POST'])
def display_login():
    next_url = request.args.get('next') or request.form.get('next')
    loginstate = False
    loginstate = login()
    print(loginstate)
    if loginstate == True:
        print('login status: ', loginstate)
        return redirect(next_url or url_for('index'))
    else:
        print('login status: ', loginstate)
        return render_template('shared/login.html', next_url=next_url)"""


def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('blog.display_login', next=request.path))

    return inner


@blueprint.route('/capstone')
@login_required
@response(template_file='capstone/staffingdata.html')
def index():
    return {}


"""@blueprint.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('home.index'))
    return render_template('shared/logout.html')"""
