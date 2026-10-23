import requests


def start_oauth_login(payload, config=None):
    config = config or {}
    request = {"providerId": config["provider_id"], "continueUri": payload["redirect_uri"]}
    if config.get("tenant_id"):
        request["tenantId"] = config["tenant_id"]
    response = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:createAuthUri",
                             params={"key": config["api_key"]}, json=request, timeout=30)
    response.raise_for_status()
    result = response.json()
    return {"authorization_url": result["authUri"], "session_id": result["sessionId"]}
