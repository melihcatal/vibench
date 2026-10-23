import os
import secrets
import urllib.parse
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, session

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
        "prompt": "select_account",
    },
)


@app.route("/login")
def start_oauth_login():
    redirect_uri = os.environ.get(
        "GOOGLE_REDIRECT_URI", "http://localhost:5000/callback"
    )
    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state

    nonce = secrets.token_urlsafe(32)
    session["oauth_nonce"] = nonce

    authorization_url, state = google.authorize_redirect(
        redirect_uri=redirect_uri, state=state, nonce=nonce
    )

    return redirect(authorization_url)
