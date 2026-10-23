import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")


def get_auth0_config():
    return {
        "domain": AUTH0_DOMAIN,
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
    }


def get_authorization_url(state):
    config = get_auth0_config()
    return f"https://{config['domain']}/authorize?response_type=code&client_id={config['client_id']}&redirect_uri=http://localhost:3000/callback&scope=openid profile email&state={state}"


def exchange_code_for_tokens(code):
    config = get_auth0_config()
    token_url = f"https://{config['domain']}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "code": code,
        "redirect_uri": "http://localhost:3000/callback",
    }
    response = requests.post(token_url, data=payload)
    return response.json()


def fetch_profile(access_token):
    config = get_auth0_config()
    profile_url = f"https://{config['domain']}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(profile_url, headers=headers)
    return response.json()
