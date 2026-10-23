import requests

from identity_client import Auth0Client
from identity_models import RegisterRequest, as_dict


def register_user(email: str, password: str, display_name: str | None = None):
    client = Auth0Client()
    payload = RegisterRequest(
        email=client.normalize(email), password=password, display_name=display_name
    )
    response = requests.post(
        f"{client.base_url}/dbconnections/signup",
        json={"client_id": client.client_id, **as_dict(payload)},
        headers=client.headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
