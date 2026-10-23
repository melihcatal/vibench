import requests
from uuid import uuid4


def pkce_login(payload, config=None):
    config = config or {}
    code_verifier = str(uuid4())
    code_challenge = pkce_code_challenge(code_verifier)
    request = {"providerId": config["provider_id"], "continueUri": payload["redirect_uri"], "code_challenge": code_challenge, "code_challenge_method": "S256"}
    response = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:createAuthUri",
                              params={"key": config["api_key"]}, json=request, timeout=30)
    response.raise_for_status()
    result = response.json()
    return {"authorization_url": result["authUri"], "session_id": result["sessionId"], "code_verifier": code_verifier}


def pkce_code_challenge(code_verifier):
    import hashlib
    import base64
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip("=")
    return code_challenge
