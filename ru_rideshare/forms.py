""" RU-Rideshare - Rutgers University Ridesharing Application

Forms used for the application.
"""

from wtforms import Form, TextField, PasswordField, DateTimeField, validators
from wtforms import IntegerField, DecimalField, SelectField, HiddenField
from flask_auth import LoginForm

class RequestRideForm(Form):
    """A WTForm for creating requests for rides"""
    dtime = DateTimeField("Pickup Date and Time", format="%Y-%m-%d %H:%M",
                          description="Format: YYYY-MM-DD hh:mm",
                          validators=[validators.DataRequired("Please enter " \
                                      "a pickup time")])
    pickup_lat = HiddenField("Pickup Latitude",
                           validators=[validators.DataRequired()])
    pickup_long = HiddenField("Pickup Longitude",
                           validators=[validators.DataRequired()])

    dest_lat = HiddenField("Destination Latitude",
                           validators=[validators.DataRequired()])
    dest_long = HiddenField("Destination Longitude",
                           validators=[validators.DataRequired()])
    pickup_addr = TextField("Pickup Address",
                            validators=[validators.DataRequired()])
    dest_addr= TextField("Destination Address",
                         validators=[validators.DataRequired()])
    seats = IntegerField("Number of seats needed", validators=[
                validators.DataRequired(),
                validators.NumberRange(1, 10)
            ])
    car = SelectField("Preferred type of car", choices=[
              ('None', 'No Preference'),
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
    seats = IntegerField("Number of seats needed", validators=[
                validators.DataRequired(),
                validators.NumberRange(1, 10)
            ])
    car = SelectField("Preferred type of car", choices=[
              ('car', 'Car'),
              ('truck', 'Truck'),
              ('van', 'Van'),
              ('suv', 'SUV')
          ], validators=[validators.DataRequired()])

class EditDriverForm(Form):
    """A WTForm for editing existing drivers"""
    seats = IntegerField("Number of seats needed", validators=[
                validators.DataRequired(),
                validators.NumberRange(1, 10)
            ])
    car = SelectField("Preferred type of car", choices=[
              ('car', 'Car'),
              ('truck', 'Truck'),
              ('van', 'Van'),
              ('suv', 'SUV')
          ], validators=[validators.DataRequired()])
