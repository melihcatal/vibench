import os
from typing import Any, Dict

from identity_client import aws_cognito_client, build_result, client_id, client_secret, normalize_identity, user_pool_id
from identity_models import RegisterUserRequest


def _secret_hash(username: str) -> str:
    import base64
    import hmac
    import hashlib

    secret = client_secret()
    if not secret:
        return ""
    msg = (username + client_id()).encode("utf-8")
    key = secret.encode("utf-8")
    digest = hmac.new(key, msg, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def register_user(email: str, password: str, locale: str = "en", display_name: str | None = None) -> Dict[str, Any]:
    request = RegisterUserRequest(email=email, password=password, locale=locale, display_name=display_name)
    identity = normalize_identity(request.email, request.locale)
    client = aws_cognito_client()
    attrs = [{"Name": "email", "Value": identity["email"]}]
    if request.display_name:
        attrs.append({"Name": "name", "Value": request.display_name})
    kwargs: Dict[str, Any] = {
        "ClientId": client_id(),
        "Username": identity["email"],
        "Password": request.password,
        "UserAttributes": attrs,
    }
    sh = _secret_hash(identity["email"])
    if sh:
        kwargs["SecretHash"] = sh
    result = client.sign_up(**kwargs)
    return build_result(user_pool_id=user_pool_id(), username=result.get("UserSub", identity["email"]), confirmed=result.get("UserConfirmed", False), code_delivery=result.get("CodeDeliveryDetails"), locale=identity["locale"])


def main(event: Dict[str, Any] | None = None, context: Any = None) -> Dict[str, Any]:
    event = event or {}
    return register_user(event["email"], event["password"], event.get("locale", "en"), event.get("display_name"))
