from identity_client import AUTH0_CONNECTION, auth0_api, post_json
from identity_models import EmailPasswordRegistration


def register_user(
    email: str, password: str, locale: str = "en", display_name: str = ""
):
    payload = EmailPasswordRegistration(
        email=email, password=password, locale=locale, display_name=display_name
    ).normalized()
    payload["connection"] = AUTH0_CONNECTION
    data = post_json(auth0_api("/dbconnections/signup"), payload)
    return {
        "user_id": data.get("_id") or data.get("user_id"),
        "email": data.get("email", payload["email"]),
        "locale": payload["locale"],
    }
