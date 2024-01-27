from flask import Flask, redirect, render_template, request, session
from urllib.parse import urlparse, parse_qs

from api.spotify_api import request_login, request_access_token

# Configure application
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/spotify_login/")
def spotify_login():
    # Clear the session
    session.clear()
    # Get the PKCE code challenge & client ID
    code_challenge = app.config["CODE_CHALLENGE"]
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
        response = request_login(code_challenge, redirect_uri, " ".join(scopes), client_id)
        return redirect(response.url)
    except Exception as e:
        return render_template("error.html", error=e)


@app.route("/spotify_login/callback/")
def spotify_login_callback():
    # Get the keywords passed as query arguments
    error = request.args.get("error")
    if error:
        return render_template("error.html", error=error)

    code = request.args.get("code")
    if not code:
        return render_template("error.html", error="Invalid Spotify redirect")

    # Redirect from our login request was successful, now we request an access token
    redirect_uri = "http://localhost:5000/spotify_login/callback/"
    code_verifier = app.config["CODE_VERIFIER"]
    client_id = app.config["SPOTIFY_CLIENT_ID"]
    try:
        response = request_access_token(code, redirect_uri, code_verifier, client_id)
        return render_template("homepage.html", access_token=response)
    except Exception as e:
        return render_template("error.html", error=e)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any session details
    session.clear()

    # Redirect user to login form
    return redirect("/")