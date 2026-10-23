import os
import requests
from identity_client import IdentityClient

# IBM App ID Federation configuration
APP_ID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
APP_ID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/oauth_callback")


def exchange_authorization_code_for_tokens(code):
    """Exchange an authorization code for access and ID tokens using IBM App ID."""
    client = IdentityClient(
        client_id=APP_ID_CLIENT_ID,
        client_secret=APP_ID_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        issuer="https://iam.cloud.ibm.com/identity",
    )
    token_response = client.exchange_code(code)
    # token_response typically contains access_token, id_token, refresh_token
    return token_response


def oauth_callback(request):
    """Handle the OAuth callback request, extract the code, and exchange it for tokens."""
    # In a web framework this would be a route handler receiving the request object
    # For demonstration, assume `request` has `args` or `form` with the code
    code = request.args.get("code")
    if not code:
        raise ValueError("Authorization code not found in callback")
    tokens = exchange_authorization_code_for_tokens(code)
    return tokens


# Example usage with a mock request dictionary
if __name__ == "__main__":
    # Simulated Flask-like request object for local testing
    class MockRequest:
        def __init__(self, params):
            self.args = params

    test_code = "AUTH_CODE_FROM_PROVIDER"
    mock_request = MockRequest({"code": test_code})
    tokens = oauth_callback(mock_request)
    print("Tokens received:")
    print(tokens)
