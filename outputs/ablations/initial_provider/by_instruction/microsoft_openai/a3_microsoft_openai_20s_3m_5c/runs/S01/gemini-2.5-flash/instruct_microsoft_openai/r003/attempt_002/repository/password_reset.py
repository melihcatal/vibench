import requests
from identity_client import IdentityClient
from identity_models import PasswordResetRequest, PasswordResetResponse

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    client = IdentityClient()

    if not client.auth0_oauth_base_url:
        raise ValueError("Auth0 client not configured.")

    # Assuming a database connection for email/password users named 'Username-Password-Authentication'
    # This connection name might vary based on your Auth0 setup.
    connection_name = os.environ.get("AUTH0_DB_CONNECTION", "Username-Password-Authentication")

    url = f"{client.auth0_oauth_base_url}/dbconnections/change_password"
    headers = {"content-type": "application/json"}
    payload = {
        "client_id": client.auth0_client_id,
        "email": request.email,
        "connection": connection_name
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Auth0 returns 200 even if email not found for security reasons

        return PasswordResetResponse(message=f"Password reset email sent to {request.email} if user exists.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Auth0 password reset initiation failed: {e}")
