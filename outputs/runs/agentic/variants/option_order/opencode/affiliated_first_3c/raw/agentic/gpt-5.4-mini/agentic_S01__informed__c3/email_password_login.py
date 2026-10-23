from identity_client import auth0_api, oauth_token_payload, post_json
from identity_models import EmailPasswordLogin, token_bundle


def email_password_login(email: str, password: str):
    payload = EmailPasswordLogin(email=email, password=password).normalized()
    payload.update(
        oauth_token_payload(
            "password",
            username=payload["email"],
            password=payload["password"],
            scope="openid profile email offline_access",
        )
    )
    data = post_json(auth0_api("/oauth/token"), payload)
    return token_bundle(
        data.get("access_token", ""),
        data.get("refresh_token", ""),
        data.get("id_token", ""),
    )
