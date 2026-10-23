import os
from flask import Flask, redirect, session, url_for
from identity_client import Auth0Client

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "super_secret_key"
)  # Replace with a strong secret key

auth0_client = Auth0Client()


@app.route("/login")
def login():
    state = os.urandom(16).hex()
    session["oauth_state"] = state
    authorization_url = auth0_client.get_authorization_url(state=state)
    return redirect(authorization_url)


# This file is for starting the login flow and would typically be run as part of a larger Flask application.
# For demonstration, you could run it and navigate to /login. However, you'll need the oauth_callback.py
# to complete the flow.

if __name__ == "__main__":
    # Example of how you might run this (requires environment variables set)
    # export AUTH0_DOMAIN="your-auth0-domain.auth0.com"
    # export AUTH0_CLIENT_ID="your-client-id"
    # export AUTH0_REDIRECT_URI="http://localhost:5000/callback"
    # export FLASK_SECRET_KEY="a_very_secret_key_indeed"
    # app.run(debug=True, port=5000)
    pass
