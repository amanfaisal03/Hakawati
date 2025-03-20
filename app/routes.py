from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm

def init_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.password == form.password.data:
                login_user(user)
                flash('You have successfully logged in!', 'success')
                return redirect(url_for('explore'))
            else:
                flash('Login failed. Please check your email and password.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)  # تسجيل الدخول التلقائي (اختياري)
            flash('You have successfully registered and logged in!', 'success')
            return redirect(url_for('home'))  # توجيه المستخدم إلى الصفحة الرئيسية
        return render_template('signup.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have successfully logged out!', 'success')
        return redirect(url_for('home'))

    @app.route('/explore')
    def explore():
        return render_template('explore.html')