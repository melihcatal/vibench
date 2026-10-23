from identity_client import auth0_client
from identity_models import OAuthResponse


def oauth_callback(code: str):
    response = auth0_client.token(code, "authorization_code", auth0_callback_url)
    oauth_response = OAuthResponse(
        access_token=response["access_token"],
        id_token=response["id_token"],
        expires_in=response["expires_in"],
    )
    print(f"OAuth Response: {oauth_response}")
    return oauth_response
