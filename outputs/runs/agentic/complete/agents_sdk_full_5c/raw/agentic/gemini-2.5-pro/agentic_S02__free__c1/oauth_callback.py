from flask import Flask, request, session, jsonify

from identity_client import okta_client
from identity_models import TokenData

app = Flask(__name__)


def handle_okta_callback():
    """
    Handles the callback from Okta, exchanges the authorization code for tokens.
    """
    if not okta_client:
        raise ConnectionError("Okta client not configured. Check environment variables.")

    # Extract authorization code from the request
    code = request.args.get('code')
    state = request.args.get('state')

    # Security check: validate the state parameter
    if state != session.get("okta_state"):
        return jsonify({"error": "invalid_state"}), 400
    
    # Exchange the authorization code for an access token
    token_response = okta_client.fetch_token(
        code=code,
        grant_type='authorization_code',
        redirect_uri=request.base_url,
    )

    # Validate nonce
    id_token_claims = okta_client.parse_id_token(token_response, nonce=session.get("okta_nonce"))
    if id_token_claims['nonce'] != session.get("okta_nonce"):
         return jsonify({"error": "invalid_nonce"}), 400

    # Store token data and return
    token_data = TokenData(**token_response)
    session["okta_token"] = token_data.model_dump()

    return jsonify(token_data.model_dump())


# Example route to demonstrate usage
@app.route("/callback/okta")
def callback_okta():
    return handle_okta_callback()
