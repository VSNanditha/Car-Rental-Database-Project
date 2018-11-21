import os

from flask import Flask, render_template
from . import auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def home():
        app.secret_key = 'super secret key'
        app.config['SESSION_TYPE'] = 'filesystem'
        return render_template('home.html', template_folder='templates')

    app.register_blueprint(auth.bp)

    return app
