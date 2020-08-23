from wtforms import Form, IntegerField, DecimalField, StringField, PasswordField, validators
from wtforms.validators import Length, DataRequired, Email, EqualTo

class RegisterForm(Form):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Userame', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=8, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20), EqualTo('password_confirm', 'Passwords do not match!')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=20)])
