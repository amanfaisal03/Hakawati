from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# تهيئة SQLAlchemy
db = SQLAlchemy()

# تهيئة Flask-Login
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hakawati.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import init_routes
    init_routes(app)

    with app.app_context():
        db.create_all()

    return app