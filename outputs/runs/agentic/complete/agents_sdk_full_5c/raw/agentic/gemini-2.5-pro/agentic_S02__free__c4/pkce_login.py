import os
import secrets
from flask import Flask, request, url_for, session, redirect
from identity_client import okta_client

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/pkce-login')
def pkce_login():
    """
    Starts an OAuth 2.0 Authorization Code Flow with PKCE.
    This is suitable for public clients like SPAs or mobile apps.
    """
    redirect_uri = url_for('pkce_callback', _external=True)
    
    # Generate and store code verifier
    code_verifier = secrets.token_urlsafe(64)
    session['code_verifier'] = code_verifier

    # The client uses the verifier to create the challenge
    return okta_client.authorize_redirect(
        redirect_uri=redirect_uri,
        code_challenge_method='S256',
        code_verifier=code_verifier
    )

@app.route('/pkce-callback')
def pkce_callback():
    """
    Handles the PKCE callback and exchanges code for token using the verifier.
    """
    code_verifier = session.pop('code_verifier', None)
    if not code_verifier:
        return "Error: code_verifier not found in session.", 400

    try:
        # The verifier is passed to the token exchange call
        token = okta_client.authorize_access_token(code_verifier=code_verifier)
        return f"Successfully logged in with PKCE. Token: {token}"
    except Exception as e:
        return f"An error occurred: {e}", 400

if __name__ == '__main__':
    app.run(port=5003, debug=True)
