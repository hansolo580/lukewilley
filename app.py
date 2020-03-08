from flask import Flask

app = Flask(__name__)


def main():
    register_blueprints()
    app.run(debug=True)


def register_blueprints():
    from views import home_views, blog_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(blog_views.blueprint)


if __name__ == '__main__':
    main()
else:
    register_blueprints()

#TODO: install blog format from flask-blog