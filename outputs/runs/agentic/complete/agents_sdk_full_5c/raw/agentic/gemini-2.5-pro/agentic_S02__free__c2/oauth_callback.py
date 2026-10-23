from flask import request, session, jsonify
from identity_client import get_okta_client
from identity_models import TokenResponse

def handle_okta_callback():
    """
    Handles the callback from Okta after user authentication.
    Exchanges the authorization code for an access token.
    """
    okta_client = get_okta_client()

    # Retrieve the authorization code from the request
    code = request.args.get('code')
    
    # Verify the state to prevent CSRF
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        return jsonify({"error": "Invalid state parameter"}), 400

    try:
        # Exchange the authorization code for tokens
        token_data = okta_client.fetch_token(code=code)
        
        # Store tokens securely, e.g., in the session
        session['okta_token'] = token_data
        
        # Validate and parse the token response
        token_response = TokenResponse(**token_data)

        return jsonify(token_response.model_dump())
    except Exception as e:
        # In a real app, handle exceptions more gracefully
        # Okta-specific errors may be returned by the fetch_token call
        return jsonify({"error": "Failed to fetch token from Okta", "details": str(e)}), 500
