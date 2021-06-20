import functools

import flask
from flask import (flash, redirect, render_template,
                   request, session, url_for)
from playhouse.flask_utils import get_object_or_404, object_list

from infrastructure.blog import Entry
from infrastructure.view_modifiers import response

blueprint = flask.Blueprint('blog', __name__, template_folder='templates')


@blueprint.route('/blog')
def blog():
    search_query = request.args.get('q')
    if search_query:
        query = Entry.search(search_query)
    else:
        query = Entry.public().order_by(Entry.timestamp.desc())
        print(query)
    return object_list('blog/index.html', query, search=search_query)


@blueprint.route('/blog/post')
@response(template_file='blog/post.html')
def post():
    return {}


@blueprint.route('/blog/post/<title>')
@response(template_file='blog/post.html')
def post_title():
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
                print(entry.slug)
                return redirect(url_for('blog.detail', slug=entry.slug))
            else:
                return redirect(url_for('blog.edit', slug=entry.slug))
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
    return render_template('blog/post.html', entry=entry)


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
                return redirect(url_for('blog.detail', slug=entry.slug))
            else:
                return redirect(url_for('blog.edit', slug=entry.slug))
        else:
            flash('Title and Content are required.', 'danger')

    return render_template('blog/edit.html', entry=entry)


@blueprint.route('/login/', methods=['GET', 'POST'])
def display_login():
    next_url = request.args.get('next') or request.form.get('next')
    loginstate = False
    from app import login
    loginstate = login()
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
        return redirect(url_for('home.index'))
    return render_template('blog/logout.html')

@blueprint.route('/newpost/', methods=['GET', 'POST'])
def new_markup_post():
    return render_template('blog/newmarkuppost.html')
