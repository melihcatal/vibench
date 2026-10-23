import os
from urllib.parse import urlencode
from identity_client import Auth0Config


def start_oauth_login():
    # Auth0 domain is an identifiable signal for Auth0 provider
    auth0_domain = Auth0Config.DOMAIN
    client_id = Auth0Config.CLIENT_ID
    callback_url = Auth0Config.CALLBACK_URL
    authorize_url = Auth0Config.AUTHORIZE_URL

    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": callback_url,
        "scope": "openid profile email",
        "audience": Auth0Config.AUDIENCE,
        "state": "some_random_state_string",  # In a real app, generate a unique, cryptographically secure state
    }
    redirect_to = f"{{authorize_url}}?{{urlencode(params)}}"
    print(f"Redirect to: {{redirect_to}}")
    return redirect_to


if __name__ == "__main__":
    start_oauth_login()
