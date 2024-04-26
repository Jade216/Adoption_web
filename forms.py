from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, Length

class AddPetForm(FlaskForm):
    '''form for adding pet'''
    name = StringField('Pet Name', validators = [InputRequired()])

    species = SelectField('Species', 
                           choices = [('cat', 'Cat'), ('dog', 'Dog'), ('Porcupine', 'Porcupine')])

    photo_url = StringField('Photo URL', validators = [Optional(), URL()])

    age = IntegerField('Age', 
                       validators = [Optional(), NumberRange(min=0, max=30)])

    notes = TextAreaField('Notes', validators = [Optional(), Length(min=10)])


class EditPetForm(FlaskForm):
    '''form for editing pet'''
    photo_url = StringField('Photo URL', validators = [Optional(), URL()])

    notes = TextAreaField('Notes', validators = [Optional(), Length(min=10)])

    available = BooleanField('Available?')