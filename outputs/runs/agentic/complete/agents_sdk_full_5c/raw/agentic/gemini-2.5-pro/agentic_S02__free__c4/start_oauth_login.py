from identity_client import okta_client
from flask import Flask, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/login')
def login():
    """
    Starts the Okta OAuth 2.0 Authorization Code Flow.
    """
    redirect_uri = url_for('callback', _external=True)
    session['nonce'] = os.urandom(16).hex()
    
    # The authorization URL is created against the Okta discovery document
    return okta_client.authorize_redirect(
        redirect_uri=redirect_uri,
        nonce=session['nonce']
    )

if __name__ == '__main__':
    # This is for demonstration purposes only.
    # In a real application, use a production-ready WSGI server.
    app.run(port=5000, debug=True)
