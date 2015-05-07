from flask.ext import wtf
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(wtf.Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
