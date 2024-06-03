from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Destination, Comment
from .forms import DestinationForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
# additional import:
from flask_login import login_required, current_user

destbp = Blueprint('destination', __name__, url_prefix='/destinations')

@destbp.route('/<id>')
def show(id):
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    # create the comment form
    form = CommentForm()
    # If the database doesn't return a destination, show a 404 page
    if not destination:
       abort(404)
    return render_template('destinations/show.html', destination=destination, form=form)

@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = DestinationForm()
    if form.validate_on_submit():
        image_path = check_upload_file(form)
        
        destination = Destination(
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
        db.session.add(destination)
        db.session.commit()
        flash('Successfully created new travel destination', 'success')
        return redirect(url_for('destination.show', id=destination.id))
    return render_template('destinations/create.html', form=form)


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

@destbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    # get the destination object associated to the page and the comment
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    if form.validate_on_submit():  
      # read the comment from the form
      comment = Comment(text=form.text.data, destination=destination, user=current_user) 
      # here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      # flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('destination.show', id=id))