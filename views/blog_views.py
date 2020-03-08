import flask

from infrastructure.view_modifiers import response

blueprint = flask.Blueprint('blog', __name__, template_folder='templates')


@blueprint.route('/blog')
@response(template_file='blog/index.html')
def index():
    return {}


@blueprint.route('/blog/post')
@response(template_file='blog/post.html')
def testpost():
    return {}


@blueprint.route('/blog/post/<title>')
@response(template_file='blog/post.html')
def post():
    return {}


# TODO: Build blog navigation
# TODO: Build blog post display
# TODO: This: https://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/