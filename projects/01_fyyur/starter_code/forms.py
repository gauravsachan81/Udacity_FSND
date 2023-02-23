from datetime import datetime
import re
from xml.dom import ValidationErr
from flask_wtf import Form
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField
)
from wtforms.validators import (
    DataRequired,
    AnyOf,
    URL,
    Length,
    Regexp,
    ValidationError
)


state_choices = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
]

genres_choices = [
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Other', 'Other'),
]

# ------------------------------------------------------------------------------------------------------------------------------#


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state_choices
    )
    
    address = StringField(
        'address', validators=[DataRequired()]
    )

    # 21-FEB-2023 - Validation added below for review comment on V1 submission
    phone = StringField(
        # TODO implement validation logic for phone -- DONE
        'phone',
        validators=[
            DataRequired(),
            Length(12),
            Regexp(r"\d{3}[-]\d{3}[-]\d{4}$", message='Phone number is not a valid US phone number. Please enter in xxx-xxx-xxxx format.')
            ]
    )
    
    image_link = StringField(
        'image_link'
    )

    # 21-FEB-2023 - Genre Validation Func for review comments on V1 submission
    # TODO implement enum restriction -- DONE
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=genres_choices
    )
    
    facebook_link = StringField(
        'facebook_link',
        validators=[
            URL(message='Please supply a valid Facebook Link.')
        ]
    )

    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField('seeking_talent')

    seeking_description = StringField('seeking_description')


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state_choices
    )

    # 21-FEB-2023 - Validation added below for review comment on V1 submission
    phone = StringField(
        # TODO implement validation logic for phone -- DONE
        'phone',
        validators=[
            DataRequired(),
            Length(12),
            Regexp(r"\d{3}[-]\d{3}[-]\d{4}$", message='Phone number is not a valid US phone number. Please enter in xxx-xxx-xxxx format.')
            ]
    )

    image_link = StringField(
        'image_link'
    )

    # 21-FEB-2023 - Genre Validation Func for review comments on V1 submission
    
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=genres_choices
     )
    
    facebook_link = StringField(
        # TODO implement enum restriction
        # 'facebook_link', validators=[URL()]
        'facebook_link',
        validators=[
            URL(message='Please supply a valid Facebook Link.')
        ]
    )

    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField('seeking_venue')

    seeking_description = StringField(
            'seeking_description'
     )
