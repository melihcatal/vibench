from identity_client import auth0_session, load_identity_config
from identity_models import AccountRequest


def email_password_login(email: str, password: str, locale: str = "en"):
    config = load_identity_config()
    account = AccountRequest(email=email, password=password, locale=locale)
    response = auth0_session().post(
        f"https://{config.auth0_domain}/oauth/token",
        json={
            "grant_type": "password",
            "username": account.email,
            "password": account.password,
            "audience": config.auth0_audience,
            "scope": "openid profile email offline_access",
            "client_id": config.auth0_client_id,
            "client_secret": config.auth0_client_secret,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
