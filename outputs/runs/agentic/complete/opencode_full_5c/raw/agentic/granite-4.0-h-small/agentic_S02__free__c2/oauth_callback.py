import identity_client
import identity_models


def oauth_callback(code):
    client = identity_client.get_client()
    # Exchange authorization code for tokens
    token_data = client.exchange_code(code)
    # Normalize and log tokens
    tokens = identity_models.normalize_token_response(token_data)
    print("Access token:", tokens["access_token"])
    print("Refresh token:", tokens["refresh_token"])
