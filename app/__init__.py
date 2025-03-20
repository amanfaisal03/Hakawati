from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# تهيئة SQLAlchemy
db = SQLAlchemy()

# تهيئة Flask-Login
login_manager = LoginManager()

def create_app():
    # إنشاء تطبيق Flask
    app = Flask(__name__)

    # تهيئة إعدادات التطبيق
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # مفتاح سري لتأمين الجلسات
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hakawati.db'  # قاعدة بيانات SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # إيقاف تنبيهات التعديلات

    # تهيئة SQLAlchemy مع التطبيق
    db.init_app(app)

    # تهيئة Flask-Login مع التطبيق
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # تحديد صفحة تسجيل الدخول

    # استيراد النماذج (Models) بعد تهيئة التطبيق
    from app.models import User

    # دالة لتحميل المستخدم (مطلوبة من قبل Flask-Login)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # استيراد المسارات (Routes) بعد تهيئة التطبيق
    from app.routes import init_routes
    init_routes(app)

    # إنشاء جداول قاعدة البيانات إذا لم تكن موجودة
    with app.app_context():
        db.create_all()

    return app