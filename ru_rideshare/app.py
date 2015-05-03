from flask import Flask, render_template, request, redirect, g
from flask_login import LoginManager, login_required, current_user, logout_user
from flask_auth import Auth

from ru_rideshare.user import User, get_user

# Create application
app = Flask(__name__)

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
app.jinja_env.globals.update(formattime=formattime)


@login_manager.user_loader
def load_user(userid):
    """Loads user object for login.
    :Parameters:
    - `userid`: An id for the user (typically a NetID).
    """
    return User(userid)


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
    return "Hello!"


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
    if request.method == "POST" and form.validate():
        # Enter request into db
        pass
    else:
        render_template("request_ride.html", form=form)


@app.route("/select_ride/<ride_id>")
def select_ride(ride_id=None):
    client = get_db_client(app, g)

    if ride_id is None:
        rides = client.get_requested_rides()
        return render_template("select_ride.html", rides=rides)

    else:
        pass
