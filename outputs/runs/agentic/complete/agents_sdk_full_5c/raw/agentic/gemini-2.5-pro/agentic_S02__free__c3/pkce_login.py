import os
import secrets
import hashlib
import base64
from flask import Flask, request, redirect, url_for
from identity_client import get_okta_client

app = Flask(__name__)

# This allows an insecure callback URL (http) for local development.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# In a real app, this would be stored in the user's session
session = {}

@app.route('/pkce-login')
def pkce_login():
    """
    Starts the Authorization Code Flow with PKCE.
    """
    okta_client = get_okta_client()
    
    # 1. Generate code_verifier
    code_verifier = secrets.token_urlsafe(64)
    session['code_verifier'] = code_verifier
    
    # 2. Generate code_challenge
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('utf-8')
    
    redirect_uri = url_for('pkce_callback', _external=True)

    # 3. Create authorization URL with PKCE parameters
    auth_url, state = okta_client.create_authorization_url(
        redirect_uri=redirect_uri,
        code_challenge=code_challenge,
        code_challenge_method='S256'
    )
    
    return redirect(auth_url)

@app.route('/pkce-callback')
def pkce_callback():
    """
    Handles the callback, exchanging the code for a token using the code_verifier.
    """
    code = request.args.get('code')
    if not code:
        return "Error: Authorization code not found.", 400

    okta_client = get_okta_client()
    
    # Retrieve the code_verifier from the session
    code_verifier = session.get('code_verifier')
    if not code_verifier:
        return "Error: Code verifier not found in session.", 400
    
    try:
        # Exchange the code for a token, providing the code_verifier
        token_data = okta_client.fetch_token(
            code=code,
            grant_type='authorization_code',
            code_verifier=code_verifier
        )
        return {
            "message": "Token successfully fetched from Okta using PKCE.",
            "access_token": token_data['access_token'][:15] + "...",
            "token_type": token_data['token_type']
        }
    except Exception as e:
        return f"An error occurred during token exchange with Okta (PKCE): {str(e)}", 500

if __name__ == '__main__':
    # To run:
    # 1. Set OKTA_* environment variables.
    # 2. Run this file.
    # 3. Navigate to http://127.0.0.1:5000/pkce-login
    app.run(port=5000, debug=True)
