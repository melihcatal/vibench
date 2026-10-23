from identity_client import auth0_request
from identity_models import UserCredentials, as_dict


def register_user(email: str, password: str) -> dict:
    credentials = UserCredentials(email=email, password=password).normalized()
    return auth0_request(
        "POST",
        "/api/v2/users",
        json={
            "email": credentials.email,
            "password": credentials.password,
            "connection": "Username-Password-Authentication",
        },
    )


def main(payload: UserCredentials) -> dict:
    return as_dict(register_user(payload.email, payload.password))
