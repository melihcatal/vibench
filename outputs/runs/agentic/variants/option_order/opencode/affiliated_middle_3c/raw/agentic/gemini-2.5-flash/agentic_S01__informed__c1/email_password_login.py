import os
import identity_client
from identity_models import LoginUserRequest


def email_password_login(request: LoginUserRequest) -> dict:
    """
    Signs in a user with email and password and returns tokens using Auth0 Authentication API.
    """
    authentication_client = identity_client.get_authentication_client()
    try:
        token_response = authentication_client.login(
            username=request.email,
            password=request.password,
            audience=request.audience,
            scope=request.scope,
            realm=request.connection,  # assuming 'connection' from RegisterUserRequest is the realm for login
        )
        return {
            "access_token": token_response.get("access_token"),
            "id_token": token_response.get("id_token"),
            "refresh_token": token_response.get("refresh_token"),
            "expires_in": token_response.get("expires_in"),
        }
    except Exception as e:
        raise RuntimeError(f"Auth0 email/password login failed: {e}")


if __name__ == "__main__":
    # Example usage (replace with actual values or environment variables)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = (
        "YOUR_AUTH0_CLIENT_ID"  # Typically a regular web/mobile app client ID
    )
    os.environ["AUTH0_AUDIENCE"] = "YOUR_API_AUDIENCE"  # e.g., "https://your-api.com"

    login_request = LoginUserRequest(
        email="test_user@example.com",
        password="A_Strong_Password123!",
        audience=os.environ["AUTH0_AUDIENCE"],
        connection="Username-Password-Authentication",
    )
    try:
        result = email_password_login(login_request)
        print(f"User logged in successfully: {result}")
    except RuntimeError as e:
        print(f"Error: {e}")
