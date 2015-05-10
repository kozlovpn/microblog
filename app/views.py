from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db
from forms import LoginForm, JokeForm
from models import User, Post, ROLE_USER, ROLE_ADMIN

login_manager = LoginManager()
login_manager.init_app(app)

#@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if g.user.is_authenticated():
        posts = g.user.posts.all()
        form = JokeForm()
        if form.validate_on_submit():
            body = form.body.data
            post = Post(body=body, author=g.user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        posts = g.user.posts.all()
        return render_template("index.html",
                               title='Home',
                               posts=posts,
                               form=form)
    else:
        flash('Please, Sign In!')
        return redirect(url_for('login'))

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
      return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        remember = form.remember_me.data
        pswd = form.password.data
        email = form.email.data
        r_user = User.query.filter_by(email=email, password=pswd).first()
        if r_user is None:
            flash('Incorrect email or password!')
        else:
            login_user(r_user, remember=remember)
            flash(r_user.id)
            flash('Logged in successfully!')
            return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        pswd = form.password.data
        email = form.email.data
        nickname = email.split('@')[0]
        user = User(nickname, pswd, email)
        r_user = User.query.filter_by(email=email).first()
        if r_user is None:
            db.session.add(user)
            db.session.commit()
            flash('User successfully registered!')
            return redirect(url_for('index'))
        else:
            flash('Error! This email already registered')
            return redirect(url_for('register'))
    else:
        return render_template('register.html',
                               title='Register',
                               form=form)

@app.before_request
def before_request():
    g.user = current_user
