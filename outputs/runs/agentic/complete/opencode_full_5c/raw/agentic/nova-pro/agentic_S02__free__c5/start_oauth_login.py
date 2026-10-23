import identity_client
import identity_models


def start_oauth_login():
    params = {
        "client_id": identity_client.CLIENT_ID,
        "redirect_uri": identity_client.REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
    }
    response = requests.get(identity_client.AUTHORIZATION_BASE_URL, params=params)
    return response.url
