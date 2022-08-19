from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class ContactForm(FlaskForm):
    name = StringField('Name or Company', validators=[DataRequired()])
    phone = StringField('Phone', validators=[])
    # phone = ''.join([c for c in str(phone) if c in {'1','2','3','4','5','6','7','8','9','0'}]) #nvm
    address = StringField('Address', validators=[])
    notes = StringField('Notes', validators=[])
    submit = SubmitField()


class SignUpForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField()