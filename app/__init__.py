import os

from flask import Flask, redirect, url_for

from . import auth, site, homepage


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

    app.register_blueprint(auth.bp)
    app.register_blueprint(site.site)
    app.register_blueprint(homepage.homepage)

    @app.route('/', methods=('GET', 'POST'))
    def home():
        app.secret_key = 'car rental'
        app.config['SESSION_TYPE'] = 'filesystem'
        app.debug = True
        return redirect(url_for('site.home'))

    return app
