from flask import Flask, redirect, url_for, session
from identity_client import get_okta_client

app = Flask(__name__)
app.secret_key = 'super-secret-key'

@app.route('/login')
def login():
    """
    Starts the OAuth 2.0 Authorization Code flow with Okta.
    """
    okta_client = get_okta_client()
    
    # Generate the authorization URL
    # The 'okta' identifier is arbitrary but used to register the client
    redirect_uri = url_for('callback', _external=True)
    authorization_url, state = okta_client.create_authorization_url(
        redirect_uri=redirect_uri
    )
    
    # Store state in session to prevent CSRF attacks
    session['oauth_state'] = state
    
    # Redirect user to Okta's login page
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    # This is a placeholder for where the callback logic would go.
    # The actual token exchange is handled in oauth_callback.py
    return "Callback received. See oauth_callback.py for implementation."

if __name__ == '__main__':
    # This is for demonstration; a real app would use a production server.
    app.run(port=8080)
