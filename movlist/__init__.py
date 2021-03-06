import os

from flask import Flask
import movlist.auth
import movlist.blog
import movlist.db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, 'movlist.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    movlist.db.init_app(app)

    # apply the blueprints to the app
    app.register_blueprint(movlist.auth.bp)
    app.register_blueprint(movlist.blog.bp)

    app.add_url_rule("/", endpoint="index")

    return app
