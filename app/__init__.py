from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(profile='dev'):
    app = Flask(__name__)

    # factory config
    from .config import config_by_name
    app.config.from_object(config_by_name[profile])

    # database init
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # name_spaces
    from .apis import api
    api.init_app(app)

    return app
