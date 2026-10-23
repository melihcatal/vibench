import os
from flask import Flask, redirect, request, url_for
from identity_client import get_okta_client

app = Flask(__name__)

# This would be stored in a secure session in a real application
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@app.route('/login')
def login():
    """
    Redirects the user to the Okta login page to start the OAuth flow.
    """
    okta_client = get_okta_client()
    
    # In a real app, the state should be generated and stored in the user's session
    # to prevent CSRF attacks.
    state = "random_state_string" 
    
    redirect_uri = url_for('callback', _external=True)
    
    # This is the Okta-specific authorization URL
    auth_url, state = okta_client.create_authorization_url(
        redirect_uri=redirect_uri,
        state=state
    )
    
    return redirect(auth_url)

@app.route('/oauth/callback')
def callback():
    # This is a placeholder for the callback handler.
    # The actual implementation is in oauth_callback.py
    return "Callback received. See oauth_callback.py for implementation."

if __name__ == '__main__':
    # This is for demonstration purposes only and is not part of the library.
    # To run:
    # 1. Set OKTA_* environment variables.
    # 2. Run this file.
    # 3. Navigate to http://127.0.0.1:5000/login
    app.run(port=5000, debug=True)
