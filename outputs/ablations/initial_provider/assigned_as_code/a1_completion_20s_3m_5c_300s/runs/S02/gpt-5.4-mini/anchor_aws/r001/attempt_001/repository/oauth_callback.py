import requests


def oauth_callback(payload, config=None):
    config = config or {}
    token_url = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": config["client_id"],
        "code": payload["code"],
        "redirect_uri": payload["redirect_uri"],
    }
    if config.get("client_secret"):
        data["client_secret"] = config["client_secret"]
    response = requests.post(token_url, data=data, timeout=15)
    response.raise_for_status()
    tokens = response.json()
    return {"tokens": tokens, "session_id": payload.get("state") or payload.get("session_id")}
