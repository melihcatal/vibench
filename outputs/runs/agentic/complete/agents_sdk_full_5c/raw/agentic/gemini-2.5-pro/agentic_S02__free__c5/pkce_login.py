import os
import secrets
import hashlib
import base64
from flask import Flask, request, redirect, session, jsonify, url_for
from identity_client import get_okta_client, PKCE_CALLBACK_URL

app = Flask(__name__)
app.secret_key = os.urandom(24)

def generate_pkce_challenge():
    """Generates a code_verifier and a corresponding S256 code_challenge."""
    code_verifier = secrets.token_urlsafe(64)
    # Using SHA256 as required by many providers, including Okta
    hashed = hashlib.sha256(code_verifier.encode('ascii')).digest()
    # Base64-urlencode the hash, removing padding
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('ascii')
    return code_verifier, code_challenge

@app.route('/pkce-login')
def pkce_login_start():
    """
    Starts the Authorization Code flow with PKCE, suitable for public clients.
    """
    scope = "openid profile email offline_access"
    
    okta_client = get_okta_client(
        redirect_uri=PKCE_CALLBACK_URL,
        scope=scope
    )

    # Generate and store PKCE verifier in the session
    code_verifier, code_challenge = generate_pkce_challenge()
    session['pkce_code_verifier'] = code_verifier
    
    authorization_url, state = okta_client.create_authorization_url(
        code_challenge=code_challenge,
        code_challenge_method='S256'
    )
    session['oauth_state'] = state
    
    return redirect(authorization_url)

@app.route('/pkce-callback')
def pkce_login_callback():
    """
    Handles the callback for the PKCE flow, exchanging the code for a token.
    """
    code = request.args.get('code')
    state = request.args.get('state')

    if not state or state != session.get('oauth_state'):
        return "State mismatch error.", 400
    
    # Retrieve the code verifier from the session
    code_verifier = session.get('pkce_code_verifier')
    if not code_verifier:
        return "Code verifier not found in session.", 400

    # Clean up session
    session.pop('oauth_state', None)
    session.pop('pkce_code_verifier', None)
    
    okta_client = get_okta_client(
        redirect_uri=PKCE_CALLBACK_URL,
        scope="openid profile email offline_access"
    )
    
    try:
        # The 'code_verifier' is passed here to complete the PKCE flow
        token_data = okta_client.fetch_token(
            code=code,
            code_verifier=code_verifier
        )
        return jsonify(token_data)
    except Exception as e:
        return f"Token exchange failed: {e}", 500
