import os
from flask import Flask, request
from identity_client import get_okta_client
from identity_models import TokenResponse

app = Flask(__name__)

# This allows an insecure callback URL (http) for local development.
# In production, you must use HTTPS.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@app.route('/oauth/callback')
def oauth_callback():
    """
    Handles the callback from Okta after user authentication.
    Exchanges the authorization code for an access token.
    """
    okta_client = get_okta_client()
    
    # The authorization code is sent as a query parameter
    code = request.args.get('code')
    if not code:
        return "Error: Authorization code not found.", 400

    try:
        # Exchange the code for a token from the Okta token endpoint
        token_data = okta_client.fetch_token(
            code=code,
            grant_type='authorization_code'
        )
        
        # Validate and structure the token response
        token_response = TokenResponse(**token_data)
        
        return {
            "message": "Token successfully fetched from Okta.",
            "access_token": token_response.access_token[:15] + "...", # Truncated for display
            "token_type": token_response.token_type
        }

    except Exception as e:
        # This will catch errors from authlib, e.g., invalid code
        return f"An error occurred during token exchange with Okta: {str(e)}", 500

if __name__ == '__main__':
    # This is for demonstration and requires running start_oauth_login.py first.
    # Set the same OKTA_* environment variables.
    app.run(port=5000, debug=True)
