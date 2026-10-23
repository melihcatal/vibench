import requests
from flask import request, redirect, session
from identity_client import IdentityClient  # local helper

# IBM App ID Federation credentials (example environment variables)
CLIENT_ID = "IBM_APPID_CLIENT_ID"
CLIENT_SECRET = "IBM_APPID_CLIENT_SECRET"
AUTH_URL = "https://iam.test.cloud.ibm.com/identity/token"
REDIRECT_URI = "http://localhost:5000/oauth/callback"

app = IdentityClient(
    base_url=AUTH_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)


def oauth_callback():
    """Callback endpoint after the user authorizes the application.

    Exchanges the authorization code for tokens and stores them in the session.
    """
    if "code" not in request.args:
        return redirect("/login?error=missing_code")
    code = request.args["code"]
    tokens = app.exchange_code_for_tokens(code, redirect_uri=REDIRECT_URI)
    session["access_token"] = tokens.get("access_token")
    session["id_token"] = tokens.get("id_token")
    session["refresh_token"] = tokens.get("refresh_token")
    return redirect("/profile")
