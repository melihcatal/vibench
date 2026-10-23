import identity_client
import identity_models


def oauth_callback(code: str) -> identity_models.OAuthResponse:
    data = {
        "client_id": identity_client.CLIENT_ID,
        "client_secret": identity_client.CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": identity_client.REDIRECT_URI,
    }
    response = requests.post(identity_client.TOKEN_URL, data=data)
    tokens = response.json()
    return identity_models.OAuthResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        id_token=tokens["id_token"],
    )
