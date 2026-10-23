from identity_client import auth0_session, load_identity_config
from identity_models import AccountRequest, normalize_email


def register_user(email: str, password: str, locale: str = "en"):
    config = load_identity_config()
    account = AccountRequest(email=email, password=password, locale=locale)
    response = auth0_session().post(
        f"https://{config.auth0_domain}/dbconnections/signup",
        json={
            "client_id": config.auth0_client_id,
            "email": normalize_email(account.email),
            "password": account.password,
            "connection": "Username-Password-Authentication",
            "user_metadata": {"locale": account.locale},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
