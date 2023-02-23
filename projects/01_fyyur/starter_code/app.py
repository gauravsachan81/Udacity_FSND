# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from sqlalchemy import desc, event
from forms import *
from flask_wtf import Form
from logging import (
    Formatter,
    FileHandler
)
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask import (
  Flask,
  render_template,
  request,
  Response,
  flash,
  redirect,
  url_for,
  abort
)
import babel
import dateutil.parser
import json
import sys
from datetime import datetime
# Start - Collections section per guidance from knowledge portal of Udacity #
import collections
import collections.abc
collections.Callable = collections.abc.Callable
# End - Collections section per guidance from knowledge portal of Udacity #
from models import db, Artist, Venue, Show
#from config import DatabaseURI

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# db=SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

app.app_context().push()

# TODO: connect to a local postgresql database  -- DONE
# SQLALCHEMY_DATABASE_URI defined in the config.py file

# ----------------------------------------------------------------------------#
# Models - Defined in Models.py
# ----------------------------------------------------------------------------#

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    print(value)
    # date=dateutil.parser.parse(value)
    # modified to handle the date / str conversion issues
    if isinstance(value, str):
        date = dateutil.parser.parse(value, ignoretz=True)
    else:
        date = value
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime
# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

# 21-FEB-2023 - Showing Venues/Artists on home page for review comments on V1
# @app.route('/')
# def index():
#    return render_template('pages/home.html')


@app.route('/')
def index():
    venues = Venue.query.order_by(desc(Venue.created_date)).limit(5).all()
    artists = Artist.query.order_by(desc(Artist.created_date)).limit(5).all()
    return render_template('pages/home.html', venues=venues, artists=artists)


# ----------------------------------------------------------------------------#
# Venues : List
# ----------------------------------------------------------------------------#


@app.route('/venues')
def venues():
    # TODO: replace with real venues data. --DONE
    #       num_upcoming_shows to be aggr on no. of upcoming shows per venue.

    try:
        data = []
        locations = db.session\
            .query(Venue)\
            .with_entities(Venue.city, Venue.state)\
            .distinct()
        for location in locations:
            location_data = {
                "city": location.city,
                "state": location.state,
                "venues": []
            }
            local_venues = db.session\
                .query(Venue)\
                .filter(Venue.city == location.city)
            for venue in local_venues:
                shows = db.session\
                    .query(Show)\
                    .filter(Show.venue_id == venue.id)\
                    .filter(Show.date_time > datetime.now())\
                    .count()
                venue_data = {
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": shows, }

                location_data["venues"].append(venue_data)

            data.append(location_data)
        return render_template('pages/venues.html', areas=data)

    except Exception as exception:
        print(exception)
        flash("Some Error happened while listing, check the logs !")

# ----------------------------------------------------------------------------#
# Venues : Search
# ----------------------------------------------------------------------------#


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on venues with partial string search.
    # Ensure it is case-insensitive. --DONE
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return
    # "The Musical Hop" and "Park Square Live Music & Coffee"
    try:
        response = {"count": 0, "data": []}

        search_term = request.form['search_term']
        print("Input Term is : "+search_term)

        search_results = db.session\
            .query(Venue)\
            .with_entities(Venue.id, Venue.name)\
            .filter(Venue.name.ilike(r"%{}%".format(search_term)))

        print("Count =", search_results.count())

        response['count'] = search_results.count()

        if search_results.count() > 0:
            for result in search_results:
                venue_info = {
                    "id": result.id,
                    "name": result.name,
                    "num_upcoming_shows": 0,
                }
                response['data'].append(venue_info)
        else:
            flash("No Venue Found for Seach Criteria " + search_term)

        return render_template(
            'pages/search_venues.html',
            results=response,
            search_term=request.form.get('search_term', '')
            )
    except Exception as exception:
        print(exception)
        flash("Some Error Occurred while searching, check the logs !")

# ----------------------------------------------------------------------------#
# Venues : Show the Venue for an ID on the FYYUR portal
# ----------------------------------------------------------------------------#


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real data from venues table, using venue_id -- DONE
    # 21-FEB-2023 - Implemented JOIN to show Past/Upcoming shows at a
    # Venue as part of the review comments on V1 submission
    try:
        data = []
        # 21-FEB-2023 - Implemented JOIN to show Past/Upcoming shows at a
        # Venue as part of the review comments on V1 submission
        past_shows = db.session.query(Artist, Show).join(Show).join(Venue)\
            .filter(
                Show.venue_id == venue_id,
                Show.artist_id == Artist.id,
                Show.date_time < datetime.now()
            )\
            .all()
        # 21-FEB-2023 - Implemented JOIN to show Past/Upcoming shows at a
        # Venue as part of the review comments on V1 submission
        print("Past Shows = ", past_shows)

        upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue)\
            .filter(
                Show.venue_id == venue_id,
                Show.artist_id == Artist.id,
                Show.date_time >= datetime.now()
            )\
            .all()
        print("Upcoming Shows = ", upcoming_shows)

        venue = Venue.query.filter_by(id=venue_id).first_or_404()

        data = {
            "id": venue.id,
            "name": venue.name,
            "city": venue.city,
            "state": venue.state,
            "genres": venue.genres,
            "address": venue.address,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_yn,
            "seeking_description": venue.seeking_desc,
            "image_link": venue.image_link,
            # 21-FEB-2023 - Implemented JOIN to show Past/Upcoming shows
            # at a Venue as part of the review comments on V1 submission
            "past_shows": [{
                'artist_id': artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.date_time.strftime("%m/%d/%Y, %H:%M")
                } for artist, show in past_shows],
            "upcoming_shows": [{
                'artist_id': artist.id,
                'artist_name': artist.name,
                'artist_image_link': artist.image_link,
                'start_time': show.date_time.strftime("%m/%d/%Y, %H:%M")
                } for artist, show in upcoming_shows],
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows)
        }
        print(data)
        print(venue.website)
        return render_template('pages/show_venue.html', venue=data)
    except Exception as exception:
        print(exception)
        flash("Error Occured while showing, check the logs !")

# ----------------------------------------------------------------------------#
# Venues : Create Venue Form
# ----------------------------------------------------------------------------#


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

# ----------------------------------------------------------------------------#
# Venues : Create a new Venue
# ----------------------------------------------------------------------------#


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead -- DONE
    # TODO: modify data to be the object returned from db insertion -- DONE
    form = VenueForm(request.form)
    venue_create_error = False
    genre_separator = ', '
    if form.validate():
        try:
            new_venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                genres=genre_separator.join(form.genres.data),
                image_link=form.image_link.data,
                website=form.website_link.data,
                facebook_link=form.facebook_link.data,
                seeking_yn=form.seeking_talent.data,
                seeking_desc=form.seeking_description.data
            )
            db.session.add(new_venue)
            db.session.commit()
            # on successful db insert, flash success
            # TODO: on unsuccessful db insert, flash an error instead. -- DONE
            # e.g., flash('An error occurred. Venue could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            flash('Venue ' + new_venue.name + ' successfully listed!')
            return render_template('pages/home.html')
        except Exception as exception:
            db.session.rollback()
            venue_create_error = True
            flash('Error !! Venue could not be listed, please try again.')
            # try to capture the error on the console for debugging
            print(exception)
        finally:
            db.session.close()
        if venue_create_error:
            return render_template('pages/home.html')
        else:
            return redirect(url_for('show_venue', venue_id=new_venue.id))
    else:
        for field,err_msgs in form.errors.items():
            flash('The field ' + field +' has following error messages-> ' + ','.join(err_msgs))
    return render_template('pages/home.html')
# ----------------------------------------------------------------------------#
# Venues : Open Venue Edit Form
# ----------------------------------------------------------------------------#


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

    # TODO: populate form with values from venue with ID <venue_id> -- DONE
    venue = Venue.query.get(venue_id)
    venue_edit_error = False
    genre_separator = ', '
    try:
        form = VenueForm(
            name=venue.name,
            city=venue.city,
            state=venue.state,
            address=venue.address,
            phone=venue.phone,
            genres=genre_separator.join(venue.genres),
            image_link=venue.image_link,
            facebook_link=venue.facebook_link,
            website_link=venue.website,
            seeking_talent=venue.seeking_yn,
            seeking_description=venue.seeking_desc
        )
        print(form.name.data)
        return render_template('forms/edit_venue.html', form=form, venue=venue)
    except Exception as exception:
        venue_edit_error = True
        flash('An error occurred. Venue could not be displayed for editing')
        # try to capture the error on the console for debugging
        print(exception)
    if venue_edit_error:
        return render_template('pages/home.html')

# ----------------------------------------------------------------------------#
# Venues : Modify the existing Venue
# ----------------------------------------------------------------------------#


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing -- DONE
    # venue record with ID <venue_id> using the new attributes
    venue_upd_form = VenueForm(request.form)
    genre_separator = ', '
    venue_edit_error = False
    print("Before Try")
    if venue_upd_form.validate():
        try:
            print("Before Venue query")
            venue = Venue.query.filter(Venue.id == venue_id).first()
            venue.name = venue_upd_form.name.data
            venue.city = venue_upd_form.city.data
            venue.state = venue_upd_form.state.data
            venue.address = venue_upd_form.address.data
            venue.phone = venue_upd_form.phone.data
            venue.genres = genre_separator.join(venue_upd_form.genres.data)
            venue.image_link = venue_upd_form.image_link.data
            venue.facebook_link = venue_upd_form.facebook_link.data
            venue.website = venue_upd_form.website_link.data
            venue.seeking_yn = venue_upd_form.seeking_talent.data
            venue.seeking_desc = venue_upd_form.seeking_description.data

            print("Before Commit")
            print(venue.website)
            print(venue.seeking_yn)
            print(venue.seeking_desc)

            db.session.commit()

            flash('Venue ' + venue_upd_form.name.data + ' successfully updated!')
            return redirect(url_for('show_venue', venue_id=venue_id))
        except Exception as exception:
            db.session.rollback()
            venue_edit_error = True
            flash('An error occured. The venue could not be updated.')
            print(exception)
        finally:
            db.session.close()
        if venue_edit_error:
            return redirect(url_for('show_venue', venue_id=venue_id))
    else:
        for field,err_msgs in venue_upd_form.errors.items():
            flash('The field ' + field +' has following error messages-> ' + ','.join(err_msgs))
    return redirect(url_for('show_venue', venue_id=venue_id))

#  ----------------------------------------------------------------
#  Venues - Delete Venue
#  ----------------------------------------------------------------


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record.
    # Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page,
    # have it so that clicking that button delete it from the db then
    # redirect the user to the homepage

    return None

#  ----------------------------------------------------------------
#  Artists : List
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database -- DONE

    try:
        artists = Artist.query.all()
        values = []
        for artist in artists:
            values.append({
                "id": artist.id,
                "name": artist.name
            })
        return render_template('pages/artists.html', artists=values)
    except Exception as exception:
        print(exception)
        flash("Error while showing Artists list, please check logs !")

# -------------------------------------------------------------------------------------#
# Artists : Search
# Implement search on venues with partial string search.
# Ensure it is case-insensitive
# -------------------------------------------------------------------------------------#


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search.
    # Ensure it is case-insensitive. -- DONE
    # seach for "A" should return "Guns N Petals","Matt Quevado",
    # and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    try:
        response = {"count": 0, "data": []}

        search_term = request.form['search_term']
        print("Input Term is : " + search_term)

        search_results = db.session\
            .query(Artist)\
            .with_entities(Artist.id, Artist.name)\
            .filter(Artist.name.ilike(r"%{}%".format(search_term)))
        print("Count  = ", search_results.count())

        response['count'] = search_results.count()

        if search_results.count() > 0:
            print("Inside IF")
            for result in search_results:
                print("Inside FOR")
                artist_info = {
                    "id": result.id,
                    "name": result.name,
                    "num_upcoming_shows": 0,
                }
                response['data'].append(artist_info)
        else:
            flash("No Artist Found for Seach Criteria " + search_term)

        return render_template(
            'pages/search_artists.html',
            results=response,
            search_term=request.form.get('search_term', '')
            )
    except Exception as exception:
        print(exception)
    flash("Some Error Occurred while searching, check the logs !")


# ----------------------------------------------------------------------------#
# Artists : Show the Artist for an ID on the FYYUR portal
# Shows the artist page with the given artist_id
# ----------------------------------------------------------------------------#


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real data from artist table, using artist_id -- DONE
    # 21-FEB-2023 - Implemented JOIN to show Past/Upcoming
    # shows at a Venue as part of the review comments on V1 submission
    try:
        print("Inside Try")
        # show_artist = []
        # show_info = []
        # past_shows = []
        # shows_past_count = 0
        # 21-FEB-2023 - Implemented JOIN to show Past/Upcoming shows
        # at a Venue as part of the review comments on V1 submission
        past_shows = db.session.query(Venue, Show).join(Show).join(Artist)\
            .filter(
                Show.venue_id == Venue.id,
                Show.artist_id == artist_id,
                Show.date_time < datetime.now()
            )\
            .all()

        # 21-FEB-2023 - Implemented JOIN to show Past/Upcoming shows
        # at a Venue as part of the review comments on V1 submission
        upcoming_shows = db.session.query(Venue, Show).join(Show).join(Artist)\
            .filter(
                Show.venue_id == Venue.id,
                Show.artist_id == artist_id,
                Show.date_time >= datetime.now()
            )\
            .all()
        # upcoming_shows=[]
        # shows_upcoming_count=0

        artist = Artist.query.filter_by(id=artist_id).first_or_404()

        print(artist)
        print("Before data setting")
        show_artist = {
            'id': artist.id,
            'name': artist.name,
            'city': artist.city,
            'state': artist.state,
            'phone': artist.phone,
            'genres': artist.genres,
            'image_link': artist.image_link,
            'website': artist.website,
            'facebook_link': artist.facebook_link,
            'seeking_venue': artist.seeking_yn,
            'seeking_description': artist.seeking_desc,
            "past_shows": [{
                'venue_id': artist.id,
                "venue_name": artist.name,
                "venue_image_link": artist.image_link,
                "start_time": show.date_time.strftime("%m/%d/%Y, %H:%M")
                } for artist, show in past_shows],
            "upcoming_shows": [{
                'venue_id': artist.id,
                'venue_name': artist.name,
                'venue_image_link': artist.image_link,
                'start_time': show.date_time.strftime("%m/%d/%Y, %H:%M")
                } for artist, show in upcoming_shows],
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows)
            }

        print("Artist Details=", show_artist)
        print("Show Artist Details =", artist.name)
        print("Outside Assignemnt")

        return render_template('pages/show_artist.html', artist=show_artist)
    except Exception as exception:
        print(exception)
        flash("Some Error Has Occured, please contact developer to resolve")

# ----------------------------------------------------------------------------#
# Artists : Open Artist Edit Form
# ----------------------------------------------------------------------------#


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

    # TODO: populate form with fields from artist with ID <artist_id> -- DONE
    artist = Artist.query.get(artist_id)
    artist_edit_error = False
    genre_separator = ', '
    try:
        form = ArtistForm(
            name=artist.name,
            city=artist.city,
            state=artist.state,
            phone=artist.phone,
            genres=artist.genres,
            website_link=artist.website,
            facebook_link=artist.facebook_link,
            seeking_venue=artist.seeking_yn,
            seeking_description=artist.seeking_desc,
            image_link=artist.image_link
        )
        print(form.name.data)
        return render_template(
            'forms/edit_artist.html', form=form, artist=artist)
    except Exception as exception:
        artist_edit_error = True
        flash('An error occurred. Artist could not be displayed for editing')
        # try to capture the error on the console for debugging
        print(exception)
    if artist_edit_error:
        return render_template('pages/home.html')

# ------------------------------------------------------------
# Artists : Modify the existing Artist
# Take values from the form submitted, and update existing
# artist record with ID <artist_id> using the new attributes
# ------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing -- DONE
    # artist record with ID <artist_id> using the new attributes
    artist_upd_form = ArtistForm(request.form)
    genre_separator = ', '
    artist_edit_error = False
    print("Before Try")
    if artist_upd_form.validate():
        try:
            print("Before Artist query")
            artist = Artist.query.filter(Artist.id == artist_id).first()
            artist.name = artist_upd_form.name.data
            artist.city = artist_upd_form.city.data
            artist.state = artist_upd_form.state.data
            artist.phone = artist_upd_form.phone.data
            artist.genres = artist_upd_form.genres.data
            artist.facebook_link = artist_upd_form.facebook_link.data
            artist.image_link = artist_upd_form.image_link.data
            artist.website = artist_upd_form.website_link.data
            artist.seeking_yn = artist_upd_form.seeking_venue.data
            artist.seeking_desc = artist_upd_form.seeking_description.data

            print("Before Artist Commit")
            print(artist.website)
            print(artist.seeking_yn)
            print(artist.seeking_desc)

            db.session.commit()

            flash('Artist '+artist_upd_form.name.data+' successfully updated!')
            return redirect(url_for('show_artist', artist_id=artist_id))
        except Exception as exception:
            db.session.rollback()
            artist_edit_error = True
            flash('An error occurred. Artist could not be updated.')
            print(exception)
        finally:
            db.session.close()
        if artist_edit_error:
            return redirect(url_for('show_artist', artist_id=artist_id))
    else:
        for field,err_msgs in artist_upd_form.errors.items():
            flash('The field ' + field +' has following error messages-> ' + ','.join(err_msgs))
    return redirect(url_for('show_artist', artist_id=artist_id))

# ----------------------------------------------------------------------------#
# Artists : Open Create Artist Form
# ----------------------------------------------------------------------------#


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

# ----------------------------------------------------------------------------#
# Artists : Create a new Artist
# ----------------------------------------------------------------------------#


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead -- DONE
    # TODO: modify data to be object returned from db insertion -- DONE

    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead. --DONE
    # e.g., flash('An error occurred. Artist ' could not be listed.')
    form = ArtistForm(request.form)
    artist_create_error = False
    genre_separator = ', '
    if form.validate():
        try:
            new_artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=genre_separator.join(form.genres.data),
                image_link=form.image_link.data,
                website=form.website_link.data,
                facebook_link=form.facebook_link.data,
                seeking_yn=form.seeking_venue.data,
                seeking_desc=form.seeking_description.data
            )
            # new_artist=Artist(name=name, city=city, state=state,
            # phone=phone, genres=genres, facebook_link=facebook_link,
            # image_link=image_link, website_link=website_link,
            # seeking_yn=seeking_yn, seeking_desc=seeking_desc)
            db.session.add(new_artist)
            db.session.commit()
            flash('Artist ' + new_artist.name + ' was successfully listed!')
            return render_template('pages/home.html')
        except Exception as exception:
            db.session.rollback()
            artist_create_error = True
            flash('Error !! Artist '+new_artist.name+' could not be listed.')
            # try to capture the error on the console for debugging
            print(exception)
        finally:
            db.session.close()
        if artist_create_error:
            return render_template('pages/home.html')
        else:
            return redirect(url_for('show_artist', artist_id=new_artist.id))
    else:
        for field,err_msgs in form.errors.items():
            flash('The field ' + field +' has following error messages-> ' + ','.join(err_msgs))
    return redirect(url_for('show_venue', artist_id=new_artist.id))
# ----------------------------------------------------------------------------#
# Shows : List
# ----------------------------------------------------------------------------#


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data. -- DONE

    try:
        show_details = []

        shows = Show.query.all()

        for show in shows:
            # artist=Artist.query.filter_by(id=show.artist_id)
            artist = Artist.query.get(show.artist_id)
            # venue=Venue.query.filter_by(id=show.venue_id)
            venue = Venue.query.get(show.venue_id)

            print("Venue Details=", venue.name)
            print("Artist Details=", artist.name)
            print("Date Time=", show.date_time.strftime("%m/%d/%Y, %H:%M:%S"))

            show_details.append({
                'id': show.id,
                'venue_id': show.venue_id,
                'venue_name': venue.name,
                'artist_id': show.artist_id,
                'artist_name': artist.name,
                'artist_image_link': artist.image_link,
                'start_time': show.date_time.strftime("%m/%d/%Y, %H:%M:%S")
                })
            print("Show Details=", show_details)

        return render_template('pages/shows.html', shows=show_details)
    except Exception as exception:
        print(exception)
        flash("Some Error occurred, please check with the developer")

# ----------------------------------------------------------------------------#
# Shows : Create Show Form
# ----------------------------------------------------------------------------#


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    show_form = ShowForm()
    return render_template('forms/new_show.html', form=show_form)

# ----------------------------------------------------------------------------#
# Shows : Create a new show
# ----------------------------------------------------------------------------#


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead -- DONE
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead. -- DONE
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    form = ShowForm(request.form)
    show_create_error = False

    try:
        new_show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            date_time=form.start_time.data
        )
        db.session.add(new_show)
        db.session.commit()
        flash('Show for Artist ID: '+form.artist_id.data + ' listed!')
        return render_template('pages/home.html')
    except Exception as exception:
        db.session.rollback()
        show_create_error = True
        flash('Error !! Venue could not be listed, please try again.')
        # try to capture the error on the console for debugging
        print(exception)
    finally:
        db.session.close()
    if show_create_error:
        return render_template('pages/home.html')

# Error Handlers
# ------------------------------------


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s \
                [in %(pathname)s:%(lineno)d]'
            )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch Application
# ----------------------------------------------------------------------------#


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port=int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
