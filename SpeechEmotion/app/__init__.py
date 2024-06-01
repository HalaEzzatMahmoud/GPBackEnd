from flask import Flask
from .database import db
from .Routes.Users import users_bp
from .Routes.Deploy import deploy_bp
from .Routes.News import News_bp
from .Routes.Complaints import Complaints_bp
from .Routes.Records import Record_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app) 

    app.register_blueprint(users_bp)
    print("Users blueprint registered") 
    app.register_blueprint(deploy_bp)
    print("Deploy blueprint registered")  
    app.register_blueprint(News_bp)
    print("News blueprint registered")  
    app.register_blueprint(Complaints_bp)
    print("Complaints blueprint registered")
    app.register_blueprint(Record_bp)
    print("Complaints blueprint registered")
    

    return app