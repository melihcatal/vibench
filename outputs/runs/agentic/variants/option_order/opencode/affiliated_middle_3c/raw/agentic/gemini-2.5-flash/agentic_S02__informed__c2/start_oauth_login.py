import os
from flask import Flask, redirect, url_for, session, request
from identity_client import Auth0Client
from identity_models import OAuthLoginRequest

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "super-secret-key"
)  # AUTH0-specific

auth0_client = Auth0Client()


@app.route("/login")
def login():
    req = OAuthLoginRequest(
        redirect_uri=url_for("callback", _external=True),
        scope=request.args.get("scope", "openid profile email"),
        audience=request.args.get("audience"),
    )
    # Store state for security (Auth0 specific)
    state = os.urandom(16).hex()
    session["oauth_state"] = state

    authorize_url = auth0_client.get_authorize_url(
        redirect_uri=req.redirect_uri,
        scope=req.scope,
        audience=req.audience,
        state=state,
    )
    return redirect(authorize_url)


if __name__ == "__main__":
    app.run(port=5000)
