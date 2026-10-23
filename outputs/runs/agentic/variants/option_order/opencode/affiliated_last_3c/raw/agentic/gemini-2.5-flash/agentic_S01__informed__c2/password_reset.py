import requests
from identity_client import Auth0Client
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest) -> Dict[str, Any]:
    client = Auth0Client()
    url = client.get_auth_url("/dbconnections/change_password")
    headers = {"Content-Type": "application/json"}
    payload = {
        "client_id": client.client_id,
        "email": request.email,
        "connection": request.connection,
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    # Auth0 returns a 200 OK with a success message in the body
    return {"message": response.text}
