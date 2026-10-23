import os
from urllib.parse import urlencode
from identity_client import IdentityClientConfig

def start_auth0_login():
    authorize_url = f"https://{{IdentityClientConfig.AUTH0_DOMAIN}}/authorize"
    params = {
        "audience": IdentityClientConfig.AUTH0_AUDIENCE,
        "scope": "openid profile email offline_access",
        "response_type": "code",
        "client_id": IdentityClientConfig.AUTH0_CLIENT_ID,
        "redirect_uri": IdentityClientConfig.AUTH0_CALLBACK_URL,
        "state": os.urandom(16).hex(), # CSRF protection
    }
    return f"{{authorize_url}}?{{urlencode(params)}}"

if __name__ == "__main__":
    login_url = start_auth0_login()
    print(f"Please visit this URL to log in: {login_url}")
