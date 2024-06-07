from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, DateField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Create new event
class EventForm(FlaskForm):
    name = StringField('Title', validators=[InputRequired()])
    images = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')
    ])
    description = TextAreaField('Description', validators=[InputRequired()])
    date = DateField('Date', validators=[InputRequired()])
    time = TimeField('Time', validators=[InputRequired()])
    venue = StringField('Venue', validators=[InputRequired()])
    ticket_price = StringField('Ticket Price', validators=[InputRequired()])
    ticket_quantity = StringField('Ticket Quantity', validators=[InputRequired()])
    status_list = ['Open', 'SoldOut', 'Inactive', 'Cancelled']
    status = SelectField('Status', choices=status_list, default=1)
    submit = SubmitField('Create Event')

# User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")

# User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')

#Booking Form
class BookingForm(FlaskForm):
    booked_events = StringField("Booked Events", validators=[InputRequired()])
    ticketQuantity = IntegerField('Ticket Quantity', [InputRequired()])
    submit = SubmitField('Book Event')
