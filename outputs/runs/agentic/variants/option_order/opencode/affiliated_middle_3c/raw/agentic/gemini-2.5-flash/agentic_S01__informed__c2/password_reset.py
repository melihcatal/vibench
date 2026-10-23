from identity_client import Auth0ManagementClient
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest) -> dict:
    client = Auth0ManagementClient()
    response = client.post(
        "api/v2/tickets/password-change",
        {
            "email": request.email,
            "connection": request.connection,
        },
    )
    response.raise_for_status()
    return response.json()
