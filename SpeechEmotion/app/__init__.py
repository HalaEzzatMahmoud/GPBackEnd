from flask import Flask
from .database import db
from .Routes.Users import users_bp
from .Routes.Deploy import deploy_bp
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app) 

    app.register_blueprint(users_bp)
    app.register_blueprint(deploy_bp)

    return app