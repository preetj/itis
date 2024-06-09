from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, makedirs
from flask_login import LoginManager
from .config import SECRET_KEY

# Initialize SQLAlchemy
db = SQLAlchemy()
DB_NAME = 'database.db'
DB_FOLDER = 'instance'  # Use Flask instance folder


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(app.instance_path, DB_NAME)}'

   

    db.init_app(app)


    # Ensure the instance folder exists
    try:
        makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating instance folder: {e}")

    # Import blueprints
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # Import models
    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app