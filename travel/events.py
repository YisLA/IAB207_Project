import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, session
from .models import Event, Comment
from .forms import EventForm, CommentForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
# additional import:
from flask_login import login_required, current_user

eventbp = Blueprint('event', __name__, url_prefix='/events')

@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    form = CommentForm()
    # If the database doesn't return an event, show a 404 page
    if not event:
       abort(404)
    return render_template('events/show.html', event=event, form=form)

@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        image_path = check_upload_file(form)
        
        event = Event(
            name=form.name.data,
            description=form.description.data,
            image=image_path,
            date=form.date.data,
            time=form.time.data,
            venue=form.venue.data,
            ticket_price=form.ticket_price.data,
            ticket_quantity=form.ticket_quantity.data,
            status=form.status.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Successfully created new event', 'success')
        return redirect(url_for('event.show', id=event.id))
    return render_template('events/create.html', form=form)


def check_upload_file(form):
    # get file data from form  
    fp = form.images.data
    filename = secure_filename(fp.filename)
    
    # get the current path of the module file… store image file relative to this path  
    BASE_PATH = os.path.dirname(__file__)
    
    # upload file location – directory of this file/static/image
    upload_dir = os.path.join(BASE_PATH, 'static', 'images')
    
    # create the directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # upload path
    upload_path = os.path.join(upload_dir, filename)
    
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/images/' + filename
    
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path

@eventbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    # get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      # read the comment from the form
      comment = Comment(text=form.text.data, event=event, user=current_user) 
      # here the back-referencing works - comment.event is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      # flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to event.show
    return redirect(url_for('event.show', id=id))

#Booking
@eventbp.route('/event_details/<event_id>/book', methods=['GET', 'POST'])
def book(event_id):
    book = BookingForm()
    event = event.query.get_or_404(event_id)
    email_id = session.get('emailid', None)

    if book.validate_on_submit():
            
        book = Event
        event = random.randint(0, 10000000000000)
        
    return render_template('book.html', userid= email_id, event=event, form=book)
