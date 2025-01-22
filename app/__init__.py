from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from app.routes import auth, user,folders,createfolder,createdeck
        app.register_blueprint(auth.bp)
        app.register_blueprint(user.bp)
        app.register_blueprint(folders.bp)
        app.register_blueprint(createfolder.bp)
        app.register_blueprint(createdeck.bp)

        db.create_all()

    return app
