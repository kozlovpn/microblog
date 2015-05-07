from flask_wtf import Form
from wtforms import TextField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    email = StringField('E-mail: ', validators=[Email(), DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)