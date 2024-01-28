from flask import Flask, redirect, render_template, request, session
from flask_caching import Cache
from uuid import uuid4
from api.spotify_api import *

# Configure application
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
# Configure cache
cache = Cache(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/spotify_login")
def spotify_login():
    # Clear the session
    session.clear()
    # Get the PKCE code challenge
    code_verifier, code_challenge = generate_code_challenge()
    # Store values in the cache
    session["id"] = uuid4()
    cache.set("session_id", session["id"])
    cache.set("code_verifier", code_verifier)
    # Get the client ID
    client_id = app.config["SPOTIFY_CLIENT_ID"]
    # Request Spotify login, will redirect the user to the specified URI
    # redirect_uri = request.base_url + "/callback/"
    redirect_uri = "http://localhost:5000/spotify_login/callback/"
    # Spotify scopes to request access for
    scopes = [
        "user-read-playback-state",
        "user-read-currently-playing",
        "playlist-read-private",
        "playlist-read-collaborative",
        "user-follow-read",
        "user-read-playback-position",
        "user-top-read",
        "user-read-recently-played",
        "user-library-read"
    ]
    try:
        response = request_login(session["id"], code_challenge, redirect_uri, " ".join(scopes), client_id)
        return redirect(response.url)
    except Exception as e:
        return render_template("error.html", error=e)


@app.route("/spotify_login/callback/")
def spotify_login_callback():
    # Check the state matches our cached session id
    state = request.args.get("state")
    if state != str(cache.get("session_id")):
        return render_template("error.html", error="Bad return state")
    
    error = request.args.get("error")
    if error:
        return render_template("error.html", error=error)

    code = request.args.get("code")
    if not code:
        return render_template("error.html", error="Invalid Spotify redirect")

    # Redirect from our login request was successful, now we request an access token
    redirect_uri = "http://localhost:5000/spotify_login/callback/"
    code_verifier = cache.get("code_verifier")
    client_id = app.config["SPOTIFY_CLIENT_ID"]
    try:
        response = request_access_token(code, redirect_uri, code_verifier, client_id)
        # Store the access token in the session
        session["token"] = response["access_token"]
        return redirect("/home")
    except Exception as e:
        return render_template("error.html", error=e)


@app.route("/home")
def home():
    # Render the user's information as a homepage
    try:
        response = get_user_info(session["token"])
        return render_template("homepage.html", user=response)
    except Exception as e:
        return render_template("error.html", error=e)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any session details
    session.clear()
    cache.clear()

    # Redirect user to login form
    return redirect("/")