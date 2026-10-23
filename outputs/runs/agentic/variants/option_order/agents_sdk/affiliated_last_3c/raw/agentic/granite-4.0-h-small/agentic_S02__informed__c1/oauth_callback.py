import os
from flask import Flask, request, redirect, abort
from identity_client import IdentityClient
from identity_models import ExchangeResult

app = Flask(__name__)

# Google Identity Platform (same-scenario)
TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'
PROFILE_ENDPOINT = 'https://openidconnect.googleapis.com/v1/userinfo'
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/oauth_callback'

@app.route('/oauth_callback', methods=['GET'])
def callback():
    # Extract query parameters sent by the IdP
    error = request.args.get('error')
    if error:
        return f"Login error: {error}", 400
    code = request.args.get('code')
    if not code:
        abort(400, description='Authorization code missing')

    # Exchange code for tokens using the client helper
    exchange = IdentityClient().exchange_authorization_code(code=code, redirect_uri=REDIRECT_URI)
    if not exchange:
        abort(500, description='Token exchange failed')
    # Fetch user profile
    profile = IdentityClient().fetch_user_profile(access_token=exchange.access_token)
    normalized = exchange.normalize_profile(profile)
    # Here you would normally create a session, set cookies, etc.
    return f"User logged in: {normalized.get('email')}"

if __name__ == '__main__':
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-123')
    app.run(host='0.0.0.0', port=5000)
