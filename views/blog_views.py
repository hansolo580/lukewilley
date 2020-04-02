import flask

from app import login
from infrastructure.blog import Entry
from infrastructure.view_modifiers import response

import functools

from flask import (Flask, abort, flash, Markup, redirect, render_template,
                   request, Response, session, url_for, app)

from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list

blueprint = flask.Blueprint('blog', __name__, template_folder='templates')


@blueprint.route('/blog')
def index():
    search_query = request.args.get('q')
    if search_query:
        query = Entry.search(search_query)
    else:
        query = Entry.public().order_by(Entry.timestamp.desc())
    return object_list('blog/index.html', query, search=search_query)


@blueprint.route('/blog/post')
@response(template_file='blog/post.html')
def testpost():
    return {}


@blueprint.route('/blog/post/<title>')
@response(template_file='blog/post.html')
def post():
    return {}


def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('blog/login', next=request.path))
    return inner


@blueprint.route('/drafts/')
@login_required
def drafts():
    query = Entry.drafts().order_by(Entry.timestamp.desc())
    return object_list('blog/index.html', query)


@blueprint.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            entry = Entry.create(
                title=request.form['title'],
                content=request.form['content'],
                published=request.form.get('published') or False)
            flash('Entry created successfully.', 'success')
            if entry.published:
                return redirect(url_for('detail', slug=entry.slug))
            else:
                return redirect(url_for('edit', slug=entry.slug))
        else:
            flash('Title and Content are required.', 'danger')
    return render_template('blog/create.html')


@blueprint.route('/<slug>/')
def detail(slug):
    if session.get('logged_in'):
        query = Entry.select()
    else:
        query = Entry.public()
    entry = get_object_or_404(query, Entry.slug == slug)
    return render_template('blog/detail.html', entry=entry)


@blueprint.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    entry = get_object_or_404(Entry, Entry.slug == slug)
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            entry.title = request.form['title']
            entry.content = request.form['content']
            entry.published = request.form.get('published') or False
            entry.save()

            flash('Entry saved successfully.', 'success')
            if entry.published:
                return redirect(url_for('detail', slug=entry.slug))
            else:
                return redirect(url_for('edit', slug=entry.slug))
        else:
            flash('Title and Content are required.', 'danger')

    return render_template('blog/edit.html', entry=entry)

# I think it's visiting the login and login result out of order
# https://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/


@blueprint.route('/login/', methods=['GET', 'POST'])
def display_login():
    next_url = request.args.get('next') or request.form.get('next')
    loginstate = False
    login()
    print(loginstate)
    if loginstate == True:
        print('login status: ', loginstate)
        return redirect(next_url or url_for('index'))
    else:
        print('login status: ', loginstate)
        return render_template('blog/login.html', next_url=next_url)



@blueprint.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('blog/login'))
    return render_template('blog/logout.html')


# TODO: This: https://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/