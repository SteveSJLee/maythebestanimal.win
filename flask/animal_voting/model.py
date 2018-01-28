from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired, Length


class CatsOrDogs(FlaskForm):
    ''' Flask form managing vote widget
    '''
    person_name = StringField("What's your name?",
                              validators=[Length(min=1, max=255,
                                                 message='Please enter' +
                                                 ' a name between' +
                                                 ' 1 and 255 characters')])
    favorite_color = StringField("What's your favorite color?",
                                 validators=[Length(min=1, max=255,
                                                    message='Please enter' +
                                                    ' a color between' +
                                                    ' 1 and 255 characters')])
    cats_or_dogs = RadioField('Do you prefer Cats or Dogs?',
                              choices=[('cats', 'Cats'),
                                       ('dogs', 'Dogs')],
                              validators=[DataRequired()])
