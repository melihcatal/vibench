import os
import flask
from flask import Flask, request, redirect
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)

@app.route('/oauth_callback')
def oauth_callback():
    # Get the authorization code from the query parameters
    code = request.args.get('code')
    if not code:
        return 'Authorization code not found', 400
    
    # Exchange the authorization code for tokens
    try:
        token_response = requests.request(
            'POST',
            'https://oauth2.googleapis.com/token',
            data={'code': code, 'client_id': os.getenv('GOOGLE_CLIENT_ID'), 'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'), 'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI'), 'grant_type': 'authorization_code'}
        )
        token_response.raise_for_status()
        tokens = token_response.json()
        
        # Verify the ID token
        id_info = id_token.verify_oauth2_token(
            tokens['id_token'],
            requests.Request(),
            os.getenv('GOOGLE_CLIENT_ID')
        )
        
        # Return the tokens
        return flask.jsonify(tokens)
    except requests.HTTPError as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)