import requests


def handle_oauth_callback(code, config=None):
    config = config or {}
    request = {
        "code": code,
        "clientId": config["client_id"],
        "clientSecret": config["client_secret"],
        "redirectUri": config["redirect_uri"]
    }
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        params={"code": code, "client_id": config["client_id"], "client_secret": config["client_secret"], "redirect_uri": config["redirect_uri"]},
        timeout=30
    )
    response.raise_for_status()
    result = response.json()
    return {"access_token": result["access_token"], "refresh_token": result["refresh_token"]}
