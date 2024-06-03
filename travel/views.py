from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination
from . import db
from flask import Blueprint, render_template

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    return render_template('index.html')

@mainbp.route('/create_event')
def create_event():
    return render_template('create_event.html')

@mainbp.route('/event_details')
def event_details():
    return render_template('event_details.html')

@mainbp.route('/bookings')
def bookings():
    return render_template('bookings.html')

@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        destinations = db.session.scalars(db.select(Destination).where(Destination.description.like(query)))
        return render_template('index.html', destinations=destinations)
    else:
        return redirect(url_for('main.index'))