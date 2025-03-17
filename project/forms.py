from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField,BooleanField
from wtforms.validators import DataRequired,length,Email,Regexp,EqualTo

class RegistrationForm(FlaskForm):
    fname = StringField('first name',validators=[DataRequired(),length(min=2,max=25)])
    lname = StringField('last name',validators=[DataRequired(),length(min=2,max=25)])
    username = StringField('username',validators=[DataRequired(),length(min=2,max=25)])
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password' , validators=[DataRequired(),Regexp(r"^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$]).{6,12}$",
               message="Password must be 6-12 characters, with at least one uppercase, one lowercase, one number, and one special character (@, #, $).")
    ])
    confirm_password = PasswordField('confirm password' , validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField("sign up")

class loginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password' , validators=[DataRequired(),Regexp(r"^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$]).{6,12}$",
               message="Password must be 6-12 characters, with at least one uppercase, one lowercase, one number, and one special character (@, #, $).")
    ])
    remember = BooleanField("Remember Me?")
    submit = SubmitField("login")


class contactForm(FlaskForm):
    name = StringField('name',validators=[DataRequired(),length(min=2,max=25)])
    email = StringField('email',validators=[DataRequired(),Email()])
    message = StringField('How can we help you? ',validators=[DataRequired(),length(min=5)])
    submit = SubmitField("send message")

