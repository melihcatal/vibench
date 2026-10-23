import secrets
from flask import Flask, redirect, url_for, session

from identity_client import okta_client

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


def start_okta_login():
    """
    Generates the authorization URL and redirects the user to Okta.
    """
    if not okta_client:
        raise ConnectionError("Okta client not configured. Check environment variables.")

    # Generate a nonce and state for security
    nonce = secrets.token_urlsafe(16)
    state = secrets.token_urlsafe(16)
    session["okta_nonce"] = nonce
    session["okta_state"] = state

    # Create the authorization URL
    redirect_uri = url_for("handle_okta_callback", _external=True)
    auth_url, _ = okta_client.create_authorization_url(
        redirect_uri=redirect_uri,
        state=state,
        nonce=nonce,
    )

    return redirect(auth_url)


# Example route to demonstrate usage
@app.route("/login/okta")
def login_okta():
    return start_okta_login()


# A dummy callback endpoint for url_for to work
@app.route("/callback/okta")
def handle_okta_callback():
    pass
