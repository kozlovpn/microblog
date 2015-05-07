from flask.ext.wtf import Form
from wtforms import TextField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    email = StringField('email', validators=[Email(), DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)