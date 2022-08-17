from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddresseeForm(FlaskForm):
    name = StringField('Name or Company', validators=[DataRequired()])
    phone = StringField('Phone', validators=[])
    # phone = ''.join([c for c in str(phone) if c in {'1','2','3','4','5','6','7','8','9','0'}]) #nvm
    address = StringField('Address', validators=[])
    submit = SubmitField()