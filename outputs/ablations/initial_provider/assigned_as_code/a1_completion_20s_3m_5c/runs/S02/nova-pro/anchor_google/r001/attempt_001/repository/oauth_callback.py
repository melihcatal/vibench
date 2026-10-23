import requests


def oauth_callback(code, config=None):
    config = config or {}
    request = {"code": code, "redirect_uri": config["redirect_uri"], "client_id": config["client_id"], "client_secret": config["client_secret"]}
    response = requests.post("https://oauth2.googleapis.com/token", data=request, timeout=30)
    response.raise_for_status()
    result = response.json()
    return {"access_token": result["access_token"], "refresh_token": result["refresh_token"]}
