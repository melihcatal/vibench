import os
import requests
from urllib.parse import urlencode

def oauth_callback(code, state, redirect_uri, config=None):
    config = config or {}
    domain = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com"
    token_url = domain + "/oauth2/token"
    client_id = config.get("client_id", os.environ.get("COGNITO_CLIENT_ID"))
    client_secret = config.get("client_secret", os.environ.get("COGNITO_CLIENT_SECRET"))

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri
    }
    if client_secret:
        data["client_secret"] = client_secret

    try:
        response = requests.post(token_url, headers=headers, data=urlencode(data))
        response.raise_for_status()
        tokens = response.json()
        return {"tokens": tokens, "session_id": state}
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "session_id": state}
