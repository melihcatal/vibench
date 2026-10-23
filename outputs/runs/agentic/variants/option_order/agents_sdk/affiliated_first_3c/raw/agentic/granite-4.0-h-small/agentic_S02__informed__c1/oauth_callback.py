import os
from urllib.parse import urlencode
from flask import Flask, request, redirect, session
from identity_client import FederatedIdentityClient

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'replace-with-strong-secret')

@app.route('/oauth/callback')
def oauth_callback():
    """Handle the provider's callback, exchange auth code for tokens, and extract claims."""
    client = FederatedIdentityClient(provider=os.getenv('FEDERATED_PROVIDER'))
    # Retrieve grant from session (saved after redirect)
    grant = session.pop('grant', None)
    if not grant:
        return 'Missing grant in session.', 400

    # Exchange auth_code for tokens
    id_token, access_token, refresh_token = client.exchange_code_for_tokens(
        grant['code'], grant['redirect_uri'], grant['state']
    )
    if not id_token:
        return 'Token exchange failed.', 500

    # Decode and normalize claims
    claims = client.decode_id_token(id_token)
    # Store data for later steps (e.g., session, DB)
    session['id_token'] = id_token
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token
    session['claims'] = claims
    return redirect('/welcome')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
