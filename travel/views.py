from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Booking
from . import db
from flask_login import current_user, login_required
import random
from datetime import datetime

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@mainbp.route('/create_event')
def create_event():
    return render_template('create_event.html')

@mainbp.route('/event_details/<int:event_id>')
def event_details(event_id):
    event = Event.query.get(event_id)
    return render_template('event_details.html', event=event)

@mainbp.route('/bookings')
@login_required
def bookings():
    user_id = current_user.id
    bookings = Booking.query.filter_by(userid=user_id).all()
    return render_template('bookings.html', bookings=bookings)

@mainbp.route('/search')
def search():
    if request.args.get('search'):
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(Event.description.like(query)))
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))

@mainbp.route('/book_event/<int:event_id>', methods=['POST'])
@login_required
def book_event(event_id):
    number_of_tickets = request.form.get('number_of_tickets')
    
    # Create a new booking with the current time as the booking_date
    new_booking = Booking(
        orderid=random.randint(1000000, 9999999),
        userid=current_user.id,
        event_id=event_id,
        number_of_tickets=number_of_tickets,
        booking_date=datetime.utcnow()
    )
    
    # Add the new booking to the database
    db.session.add(new_booking)
    db.session.commit()
    
    return redirect(url_for('main.bookings'))
