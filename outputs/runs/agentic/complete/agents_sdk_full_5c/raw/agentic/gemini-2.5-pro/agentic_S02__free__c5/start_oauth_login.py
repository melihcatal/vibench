import os
from flask import Flask, redirect, request, url_for, session
from identity_client import get_okta_client

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/login')
def start_oauth_login():
    """
    Starts the OIDC Authorization Code flow with Okta.
    """
    scope = "openid profile email offline_access"
    
    # Using a helper to construct the client
    okta_client = get_okta_client(
        redirect_uri=url_for('handle_callback', _external=True),
        scope=scope
    )
    
    # The 'state' is a security measure to prevent CSRF attacks.
    # It is stored in the session to be verified in the callback.
    authorization_url, state = okta_client.create_authorization_url()
    session['oauth_state'] = state
    
    # Redirect the user's browser to Okta's authorization endpoint
    return redirect(authorization_url)

@app.route('/callback')
def handle_callback():
    # This is a placeholder for the callback handler logic
    # The full implementation is in oauth_callback.py
    return "Callback received. See oauth_callback.py for implementation.", 200

# To run this example:
# 1. Set environment variables: OKTA_CLIENT_ID, OKTA_CLIENT_SECRET, OKTA_ISSUER_URL
# 2. Run the Flask app: flask run
# 3. Navigate to http://localhost:5000/login
