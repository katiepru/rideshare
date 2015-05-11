from flask import Flask, render_template, request, redirect, g
from flask_login import LoginManager, login_required, current_user, logout_user
from flask_auth import Auth
import json

# Create application
app = Flask(__name__)

from ru_rideshare.user import User, get_user
from ru_rideshare.util import set_logger, get_db_client
from ru_rideshare.forms import RULoginForm, RequestRideForm, AddDriverForm
from ru_rideshare.forms import EditDriverForm

# Import settings in config.py
app.config.from_pyfile("config.py", silent=True)
app.secret_key = app.config['SECRET_KEY']

# Initialize logging
set_logger(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

# Allows us to use the function in our templates
#app.jinja_env.globals.update(formattime=formattime)


@login_manager.user_loader
def load_user(userid):
    """Loads user object for login.
    :Parameters:
    - `userid`: An id for the user (typically a NetID).
    """
    client = get_db_client(app, g)
    d = client.is_driver(userid)
    return User(userid, d)


def render_login(**kwargs):
    """Renders the login template.
    Takes a WTForm in the keyword arguments.
    """
    return render_template('login.html', **kwargs)


def login_success(user):
    """Function executed on successful login.
    Redirects the user to the homepage.
    :Parameters:
    - `user`: The user that has logged in.
    """
    return redirect('/')


# Views

@app.route("/")
@login_required
def index():
    return str(current_user.driver)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Handles authentication."""
    a = Auth(app.config['AUTH'], get_user)
    return a.login(request, RULoginForm, render_login, login_success)


@app.route("/logout")
@login_required
def logout():
    """Handles logging out."""
    logout_user()
    return redirect('/')


@app.route("/request_ride", methods=["GET", "POST"])
def request_ride():
    form = RequestRideForm(request.form)
    if request.method == 'POST':
        for field in form:
            print(str(field.label) + ": " + str(field.data))
    if request.method == "POST" and form.validate():
        print("IN HERE")
        client = get_db_client(app, g)
        if form.car.data == 'None':
            form.car.data = None
        client.insert_request(current_user.id, form.dtime.data,
                (form.pickup_lat.data, form.pickup_long.data),
                (form.dest_lat.data, form.dest_long.data), form.seats.data,
                form.car.data)
        return render_template("request_ride.html", form=form, msg="Success!")
    else:
        return render_template("request_ride.html", form=form)


@app.route("/add_driver", methods=["GET", "POST"])
def add_driver():
    form = AddDriverForm(request.form)
    if request.method == "POST" and form.validate():
        client = get_db_client(app, g)
        client.insert_driver(current_user.id, form.name.data, form.car.data,
                             int(form.seats.data))
        current_user.driver = True
        return render_template("add_driver.html", form=form, msg="Success!")
    else:
        return render_template("add_driver.html", form=form)


@app.route("/edit_driver", methods=["GET", "POST"])
def edit_driver():
    form = EditDriverForm(request.form)
    if request.method == "POST" and form.validate():
        client = get_db_client(app, g)
        client.insert_driver(current_user.id, form.car.data, form.seats.data)
        return render_template("edit_driver.html", form=form, msg="Success!")
    else:
        return render_template("edit_driver.html", form=form)


@app.route("/view_requests")
def view_requests():
    return render_template("view_requests.html")


@app.route("/get_rides", methods=["POST"])
def get_rides():
    client = get_db_client(app, g)
    res = client.find_requests(request.form)
    print(res)
    return '{"rides" : %s}' % (json.dumps(res))


@app.route("/requests/<rid>", methods=["POST"])
def requests(rid=None):
    client = get_db_client(app, g)
    client.accept_request(current_user.netid, rid);
    print("Accepted request %s", rid);
    return "{}"
