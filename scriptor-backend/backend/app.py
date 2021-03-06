from flask import Flask, request, g, jsonify

app = Flask(__name__)

# Create the indices/mappings for all the models
from backend.users.models import User
from backend.search.models import PodcastTranscriptionBlob
from backend.podcasts.models import Podcast


def init_db():
    User.init()
    PodcastTranscriptionBlob.init()
    Podcast.init()


init_db()

# Middleware to run before each request
@app.before_request
def before_each_request():
    # Try to get & set the current user if an auth token has been provided.
    auth_token = request.headers.get("Authorization")

    try:
        auth_token = auth_token.replace("Bearer ", "")
        g.current_user = User.get_user_by_authtoken(auth_token=auth_token)
    except Exception as e:
        g.current_user = None


@app.route("/")
def index():
    # A dummy API endpoint for checking the status of the API
    return jsonify(success=True)

# Import all blueprints
from backend.users import users_blueprint
from backend.search import search_blueprint
from backend.podcasts import podcasts_blueprint

app.register_blueprint(users_blueprint)  # This handles all user profile-related API calls
app.register_blueprint(search_blueprint)  # This handles all search-based API calls
app.register_blueprint(podcasts_blueprint)  # This handles all podcast-based API calls
