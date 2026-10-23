from identity_client import GoogleIdentityClient
from identity_models import normalize_email


def password_reset(email: str):
    client = GoogleIdentityClient()
    response = client.session.post(
        "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode",
        params={"key": client.key},
        json={"requestType": "PASSWORD_RESET", "email": normalize_email(email)},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
