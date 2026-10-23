import os
from flask import Flask, request, session, jsonify, url_for
from identity_client import get_okta_client
from identity_models import TokenData

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/callback')
def oauth_callback():
    """
    Handles the OAuth callback from the identity provider (Okta).
    Exchanges the authorization code for an access token.
    """
    # Retrieve the authorization code and state from the query parameters
    code = request.args.get('code')
    state = request.args.get('state')

    # Verify the state to prevent CSRF attacks
    if not state or state != session.get('oauth_state'):
        return "State mismatch error.", 400

    # Clean up the state from the session
    session.pop('oauth_state', None)

    # Initialize the Okta client
    scope = "openid profile email offline_access"
    okta_client = get_okta_client(
        redirect_uri=url_for('oauth_callback', _external=True),
        scope=scope
    )

    try:
        # Exchange the authorization code for tokens
        token_data = okta_client.fetch_token(code=code)
        
        # Store tokens securely in the session (in a real app, use a more secure store)
        session['token_data'] = token_data

        # Validate and store token data using a Pydantic model
        validated_tokens = TokenData.parse_obj(token_data)

        return jsonify({
            "message": "Login successful",
            "access_token_type": validated_tokens.token_type,
            "scope": validated_tokens.scope,
            "expires_in": validated_tokens.expires_in
        })

    except Exception as e:
        # Handle exceptions, e.g., invalid code
        return f"An error occurred during token exchange: {e}", 500

# This file is intended to be run as part of the same Flask application
# as start_oauth_login.py.
