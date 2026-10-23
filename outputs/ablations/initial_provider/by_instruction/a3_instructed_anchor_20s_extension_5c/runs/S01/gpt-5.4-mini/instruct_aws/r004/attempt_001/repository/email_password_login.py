from typing import Any, Dict

from identity_client import aws_cognito_client, build_result, client_id, client_secret, normalize_identity
from identity_models import LoginRequest


def _secret_hash(username: str) -> str:
    import base64
    import hashlib
    import hmac

    secret = client_secret()
    if not secret:
        return ""
    digest = hmac.new(secret.encode("utf-8"), (username + client_id()).encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def email_password_login(email: str, password: str) -> Dict[str, Any]:
    request = LoginRequest(email=email, password=password)
    identity = normalize_identity(request.email)
    client = aws_cognito_client()
    auth = {"USERNAME": identity["email"], "PASSWORD": request.password}
    sh = _secret_hash(identity["email"])
    if sh:
        auth["SECRET_HASH"] = sh
    result = client.initiate_auth(AuthFlow="USER_PASSWORD_AUTH", AuthParameters=auth, ClientId=client_id())
    return build_result(authentication_result=result.get("AuthenticationResult", {}), challenge_name=result.get("ChallengeName"), session=result.get("Session"), locale=identity["locale"])


def main(event: Dict[str, Any] | None = None, context: Any = None) -> Dict[str, Any]:
    event = event or {}
    return email_password_login(event["email"], event["password"])
