from flask import Flask, render_template, flash
from db import db, Person, db_exceptions
import logging
from os import environ
from sys import stdout
from model import CatsOrDogs

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(stdout))
app.logger.setLevel(logging.DEBUG)

try:
    app.secret_key = environ['FLASK_SECRET_KEY']
except:
    app.secret_key = 'development'


# Database connection management
@app.before_request
def _db_connect():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


def create_tables():
    ''' Attempts to initialize database table. If it exists, db returns
        OperationalError; continue
    '''
    try:
        with db.transaction():
            db.create_tables([Person])
        app.logger.debug('Database tables initialized')

    except db_exceptions['OperationalError']:
        app.logger.debug('Database tables already initialized')
        pass

    except Exception as e:
        app.logger.error('Database error: {}'.format(str(e)))


def write_to_db(person_name_input,
                favorite_color_input,
                favorite_animal_input):
    # Writes data to database. Returns message passed from database.
    try:
        with db.transaction():
            ''' Attempt to add the vote. If person_name is taken,
                the database will raise an IntegrityError
            '''
            Person.create(
                person_name=person_name_input,
                favorite_color=favorite_color_input,
                favorite_animal=favorite_animal_input
            )

        return "Thank you for voting!"

    except db_exceptions['IntegrityError']:
        return "You have already voted!"

    except Exception as e:
        app.logger.error('Exception in write_to_db: {}'.format(str(e)))
        return "Please try again later."


@app.route('/', methods=['GET', 'POST'])
def index_page():
    # Displays index page with vote widget.

    form = CatsOrDogs()

    if form.validate_on_submit():
        result = write_to_db(person_name_input=form.person_name.data,
                             favorite_color_input=form.favorite_color.data,
                             favorite_animal_input=form.cats_or_dogs.data)
        flash(result)

    else:
        for field, error in form.errors.items():
            flash('Please doublecheck your input: {}'.format(error[0]))

    return render_template('index.html', form=form)


if __name__ == '__main__':
    create_tables()
    app.run()
