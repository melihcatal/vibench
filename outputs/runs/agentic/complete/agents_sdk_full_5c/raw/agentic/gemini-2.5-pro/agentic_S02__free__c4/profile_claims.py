from identity_client import okta_client
from identity_models import UserProfile
from flask import Flask, session, jsonify, abort

app = Flask(__name__)

def get_user_from_session():
    """Helper to retrieve user token from session."""
    user_token = session.get('user_token')
    if not user_token:
        abort(401, "User not logged in.")
    return user_token

@app.route('/profile')
def profile():
    """
    Fetches the user's profile claims from the Okta userinfo endpoint.
    """
    user_token = get_user_from_session()
    
    # `userinfo` is a method from authlib that calls the OIDC userinfo endpoint
    # which is discovered from the Okta .well-known/openid-configuration endpoint.
    user_info_claims = okta_client.userinfo(token=user_token)

    # Validate and normalize the claims using a Pydantic model
    try:
        profile = UserProfile(**user_info_claims)
        return jsonify(profile.model_dump())
    except Exception as e:
        return f"Error parsing claims: {e}", 500

if __name__ == '__main__':
    # For demonstration, requires a running session from the callback handler.
    # This would typically be part of the same Flask application.
    app.secret_key = "a_secret_key_for_session" 
    app.run(port=5002, debug=True)
