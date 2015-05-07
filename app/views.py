from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
	{
	    'author': { 'nickname': 'John' },
	    'body': 'Beautiful day in Portland!'
	},
	{
	    'author': { 'nickname': 'Susan' },
	    'body': 'The Avengers movie was so cool!'
	}
    ] 
    return render_template("index.html",
	title = 'Home',
	user = user,
	posts = posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        pswd = form.password.data
        email = form.email.data
        r_user_email = User.query.filter_by(email=email).first()
    return render_template('login.html',
                           title='Sign In',
                           form=form)

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
            flash('Error! This email alredy registered')
            return redirect(url_for('register'))
    else:
        return render_template('register.html',
                                title='Register',
                                form=form)

#@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
            user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
            db.session.add(user)
            db.session.commit()
        remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user
