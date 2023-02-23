import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


#class DatabaseURI:

    # TODO IMPLEMENT DATABASE URL -- DONE
    # SQLALCHEMY_DATABASE_URI = '<Put your local database url>'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:noida$2023@localhost:5432/example'
    # 21-FEB-2023 - changed as part of the review comment on V1 submission

    # Just change names of your db and crendtials to connect to local db
    # DATABASE_NAME = "example"
    # username = 'postgres'
    # password = 'noida$2023'
    # url = 'localhost:5432'
    # SQLALCHEMY_DATABASE_URI = "postgres://{}:{}@{}/{}".format(username, password, url, DATABASE_NAME)
