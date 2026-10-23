from flask import Flask, session, jsonify, request
import httpx
from identity_client import OKTA_ISSUER_URL
from identity_models import UserProfile

app = Flask(__name__)

def fetch_profile_claims(access_token: str) -> dict:
    """
    Fetches user profile claims from the OIDC userinfo endpoint.
    
    Args:
        access_token: The access token obtained from the token exchange.
        
    Returns:
        A dictionary containing the user's profile claims.
    """
    if not OKTA_ISSUER_URL:
        raise ValueError("OKTA_ISSUER_URL is not configured.")

    # Okta's userinfo endpoint is part of the OIDC standard
    userinfo_endpoint = f"{OKTA_ISSUER_URL}/v1/userinfo"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    
    with httpx.Client() as client:
        response = client.get(userinfo_endpoint, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP error codes
        return response.json()

@app.route('/profile')
def get_profile():
    """
    An example endpoint to fetch and display the user's profile.
    Assumes token data is stored in the session after a successful login.
    """
    token_data = session.get('token_data')
    if not token_data or 'access_token' not in token_data:
        return "Not authenticated. Please log in first.", 401

    try:
        claims = fetch_profile_claims(token_data['access_token'])
        
        # Normalize the claims into our local UserProfile model
        # This provides a consistent data structure regardless of the provider
        user_profile = UserProfile.parse_obj(claims)
        
        return user_profile.json()
        
    except httpx.HTTPStatusError as e:
        return f"Failed to fetch profile: {e.response.status_code} - {e.response.text}", 500
    except Exception as e:
        return f"An error occurred: {e}", 500
