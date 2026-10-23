from typing import Any, Dict

from identity_client import aws_cognito_client, build_result, client_id, client_secret, normalize_identity
from identity_models import PasswordResetRequest


def _secret_hash(username: str) -> str:
    import base64
    import hashlib
    import hmac

    secret = client_secret()
    if not secret:
        return ""
    digest = hmac.new(secret.encode("utf-8"), (username + client_id()).encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def password_reset(email: str) -> Dict[str, Any]:
    request = PasswordResetRequest(email=email)
    identity = normalize_identity(request.email)
    client = aws_cognito_client()
    params: Dict[str, str] = {"ClientId": client_id(), "Username": identity["email"]}
    sh = _secret_hash(identity["email"])
    if sh:
        params["SecretHash"] = sh
    result = client.forgot_password(**params)
    return build_result(code_delivery=result.get("CodeDeliveryDetails"), locale=identity["locale"])


def main(event: Dict[str, Any] | None = None, context: Any = None) -> Dict[str, Any]:
    event = event or {}
    return password_reset(event["email"])
