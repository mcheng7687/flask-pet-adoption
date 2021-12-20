from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import InputRequired, Optional, Email, NumberRange, URL

class AddPetForm(FlaskForm):
    """Form to add new pet"""

    name = StringField("Name", validators=[InputRequired()])
    species = SelectField("Species", choices=[("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine")], validators=[InputRequired()])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[NumberRange(min=0, max=30, message='Invalid length')])
    notes = StringField("Notes", validators=[Optional()])

class EditPetForm(FlaskForm):
    """Form to edit pets"""

    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = StringField("Notes", validators=[Optional()])
    available = BooleanField("Availability")