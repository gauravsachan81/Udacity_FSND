# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
# 21-FEB-2023 Added as part of suggestions on Code Review for V1 submission
from sqlalchemy.sql import func

db = SQLAlchemy()

# #####################  Model Definitions  ###################################
# ----------------------------------------------------------------------------#
# Venue
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(250))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(250))
    facebook_link = db.Column(db.String(120))
    seeking_yn = db.Column(db.Boolean, default=False)
    seeking_desc = db.Column(db.String(1000))
    # 21-FEB-2023 Added as part of suggestions on Code Review for V1 submission
    created_date = db.\
        Column(db.DateTime(timezone=True), server_default=func.now())
    updated_date = db.\
        Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<Venue: {self.id}, Name: {self.name}>'

# ----------------------------------------------------------------------------#
# Artist
# ----------------------------------------------------------------------------#


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(250))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(250))
    facebook_link = db.Column(db.String(120))
    seeking_yn = db.Column(
        db.Boolean, default=False)
    seeking_desc = db.Column(db.String(1000))
    # 21-FEB-2023 Added as part of suggestions on Code Review for V1 submission
    created_date = db.Column(
        db.DateTime(timezone=True), server_default=func.now())
    updated_date = db.Column(
        db.DateTime(timezone=True), onupdate=func.now())

    # Capture log info for debugging
    def __repr__(self):
        return f'<Artist: {self.id}, Name: {self.name}>'

# ----------------------------------------------------------------------------#
# Show
# ----------------------------------------------------------------------------#


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(
        db.Integer, primary_key=True)
    date_time = db.Column(
        db.DateTime, nullable=False)
    artist_id = db.Column(
        db.Integer, db.ForeignKey('artists.id'), nullable=False)
    artist = db.relationship(
        'Artist', backref=db.backref('shows', cascade='all,delete'))
    venue_id = db.Column(
        db.Integer, db.ForeignKey('venues.id'), nullable=False)
    venue = db.relationship(
        'Venue', backref=db.backref('shows', cascade='all,delete'))

    # Capture log info for debugging
    def __repr__(self):
        return f'<Show: {self.id},\
            Date_Time: {self.date_time},\
                Artist: {self.artist_id},\
                    Venue: {self.venue_id}>'
