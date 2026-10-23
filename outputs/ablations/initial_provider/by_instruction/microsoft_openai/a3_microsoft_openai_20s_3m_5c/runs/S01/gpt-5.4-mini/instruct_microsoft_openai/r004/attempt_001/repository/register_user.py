from identity_client import microsoft_headers, post_json
from identity_models import UserIdentityRequest, coerce_response


def register_user(email: str, password: str, display_name: str = None, locale: str = None):
    req = UserIdentityRequest(email=email, password=password, display_name=display_name, locale=locale)
    payload = req.normalized()
    payload["passwordProfile"] = {"password": payload.pop("password"), "forceChangePasswordNextSignIn": True}
    payload["accountEnabled"] = True
    payload["mailNickname"] = payload["email"].split("@")[0]
    result = post_json("https://graph.microsoft.com/v1.0/users", payload, headers=microsoft_headers())
    return coerce_response(result)
