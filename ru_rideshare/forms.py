""" RU-Rideshare - Rutgers University Ridesharing Application

Forms used for the application.
"""

from wtforms import Form, TextField, PasswordField, DateTimeField, validators
from wtforms import IntegerField, DecimalField, SelectField
from flask_auth import LoginForm

class RequestForm(Form):
    """A WTForm for creating requests"""
    dtime = DateTimeField("Pickup Date and Time", format="%Y-%m-%d %H:%M:%S",
                          validators=[validators.DataRequired("Please enter " \
                                      "a pickup time")])
    pickup_lat = DecimalField("Pickup Latitude", places=6,
                           validators=[validators.DataRequired()])
    pickup_long = DecimalField("Pickup Longitude",
                           validators=[validators.DataRequired()])

    dest_lat = DecimalField("Destination Latitude", places=6,
                           validators=[validators.DataRequired()])
    dest_long = DecimalField("Destination Longitude", places=6,
                           validators=[validators.DataRequired()])
    seats = IntegerField("Number of seats needed", validators=[
                validators.DataRequired(),
                validators.NumberRange(1, 10)
            ])
    car = SelectField("Preferred type of car", choices=[
              ('car', 'Car'),
              ('truck', 'Truck'),
              ('van', 'Van'),
              ('suv', 'SUV')
          ])


class RULoginForm(LoginForm):
    """A WTForm representing the login form."""
    username = TextField('Netid', validators=[validators.DataRequired()])
    password = PasswordField('Password',
            validators=[validators.DataRequired()])


class AddDriverForm(Form):
    """A WTForm for adding new drivers"""
    name = TextField("Name", validators=[validators.DataRequired()])
    car = SelectField("Preferred type of car", choices=[
              ('car', 'Car'),
              ('truck', 'Truck'),
              ('van', 'Van'),
              ('suv', 'SUV')
          ], validators=[validators.DataRequired()])
    seats = IntegerField("Number of seats needed", validators=[
                validators.DataRequired(),
                validators.NumberRange(1, 10)
            ])

class EditDriverForm(Form):
    """A WTForm for editing existing drivers"""
    car = SelectField("Preferred type of car", choices=[
              ('car', 'Car'),
              ('truck', 'Truck'),
              ('van', 'Van'),
              ('suv', 'SUV')
          ], validators=[validators.DataRequired()])
    seats = IntegerField("Number of seats needed", validators=[
                validators.DataRequired(),
                validators.NumberRange(1, 10)
            ])
