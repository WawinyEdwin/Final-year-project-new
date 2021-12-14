from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,InputRequired, Length, EqualTo, Email
class RegistrationForm(FlaskForm):
    username = StringField(label="Username", validators = [DataRequired(), Length(min=4, max=14 )])
    email = StringField(label = "Email",validators = [DataRequired(), Email()])
    password = PasswordField("Password", [InputRequired(), Length(min=6,max=16), EqualTo('confirm_password', message='Passwords must match')] )
    confirm_password = PasswordField("Confirm Password",[InputRequired(),Length(min=6, max=16)])
    submit = SubmitField(label = "Sign Up")

class LoginForm(FlaskForm):
    email = StringField(label = "Email",validators = [DataRequired(), Email()])
    password = PasswordField(label = "Password", validators = [DataRequired(), Length(min=6,max=16)] )
    submit = SubmitField(label = "Sign In")