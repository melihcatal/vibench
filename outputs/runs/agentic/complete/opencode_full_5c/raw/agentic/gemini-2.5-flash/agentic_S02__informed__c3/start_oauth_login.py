import os
from flask import Flask, redirect, url_for, session, request
from identity_client import build_authorization_url

# Google Identity Platform OIDC integration
# Provider-identifying signal: GOOGLE_OAUTH_AUTH_URL in identity_client.py

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")


@app.route("/login/google")
def start_oauth_login():
    """Starts the Google OAuth authorization-code login flow."""
    # A real application would generate a secure, unique state parameter.
    # For this example, we use a simple string.
    state = os.urandom(16).hex()
    session["oauth_state"] = state

    scope = ["openid", "email", "profile"]
    auth_url = build_authorization_url(scope=scope, state=state, pkce_enabled=False)
    return redirect(auth_url)


if __name__ == "__main__":
    # Example usage: http://127.0.0.1:5000/login/google
    app.run(debug=True)
