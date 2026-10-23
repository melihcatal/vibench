import requests
import hashlib
import secrets


def pkce_login(payload, config=None):
    config = config or {}
    code_verifier = secrets.token_urlsafe(96)
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode()
    request = {"providerId": config["provider_id"], "continueUri": payload["redirect_uri"], "code_challenge": code_challenge, "code_challenge_method": "S256"}
    response = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:createAuthUri",
                             params={"key": config["api_key"]}, json=request, timeout=30)
    response.raise_for_status()
    result = response.json()
    return {"authorization_url": result["authUri"], "session_id": result["sessionId"], "code_verifier": code_verifier}