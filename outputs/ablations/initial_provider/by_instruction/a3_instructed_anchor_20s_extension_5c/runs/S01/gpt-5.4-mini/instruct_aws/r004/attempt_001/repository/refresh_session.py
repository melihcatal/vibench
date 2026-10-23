from typing import Any, Dict

from identity_client import aws_cognito_client, build_result, client_id, client_secret
from identity_models import RefreshRequest


def _secret_hash(username: str) -> str:
    import base64
    import hashlib
    import hmac

    secret = client_secret()
    if not secret:
        return ""
    digest = hmac.new(secret.encode("utf-8"), (username + client_id()).encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def refresh_session(refresh_token: str, username: str | None = None) -> Dict[str, Any]:
    request = RefreshRequest(refresh_token=refresh_token)
    client = aws_cognito_client()
    params: Dict[str, str] = {"REFRESH_TOKEN": request.refresh_token}
    if username:
        sh = _secret_hash(username)
        if sh:
            params["SECRET_HASH"] = sh
        params["USERNAME"] = username
    result = client.initiate_auth(AuthFlow="REFRESH_TOKEN_AUTH", AuthParameters=params, ClientId=client_id())
    return build_result(authentication_result=result.get("AuthenticationResult", {}), challenge_name=result.get("ChallengeName"), session=result.get("Session"))


def main(event: Dict[str, Any] | None = None, context: Any = None) -> Dict[str, Any]:
    event = event or {}
    return refresh_session(event["refresh_token"], event.get("username"))
