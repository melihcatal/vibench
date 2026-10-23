import requests
from identity_client import load_identity_config
from identity_models import UserRegistrationRequest, as_payload, normalize_registration


def register_user(email: str, password: str, name: str | None = None, locale: str | None = None) -> dict:
    config = load_identity_config()
    data = normalize_registration({"email": email, "password": password, "name": name, "locale": locale})
    payload = as_payload(UserRegistrationRequest(email=data.email, password=data.password or "", name=data.name, locale=data.locale))
    payload["connection"] = config.auth0_connection
    payload["email_verified"] = False
    response = requests.post(f"https://{config.auth0_domain}/api/v2/users", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
