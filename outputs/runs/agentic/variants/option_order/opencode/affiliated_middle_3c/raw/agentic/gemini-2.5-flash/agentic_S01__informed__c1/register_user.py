import os
import identity_client
from identity_models import RegisterUserRequest


def register_user(request: RegisterUserRequest) -> dict:
    """
    Registers a new email/password user account using Auth0 Management API.
    """
    management_client = identity_client.get_management_client()
    user_data = {
        "email": request.email,
        "password": request.password,
        "connection": request.connection,
        "email_verified": False,
    }
    try:
        new_user = management_client.users.create(user_data)
        return {"user_id": new_user["user_id"], "email": new_user["email"]}
    except Exception as e:
        raise RuntimeError(f"Auth0 user registration failed: {e}")


if __name__ == "__main__":
    # Example usage (replace with actual values or environment variables)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_MANAGEMENT_CLIENT_ID"] = "YOUR_AUTH0_MANAGEMENT_CLIENT_ID"
    os.environ["AUTH0_MANAGEMENT_CLIENT_SECRET"] = "YOUR_AUTH0_MANAGEMENT_CLIENT_SECRET"

    user_request = RegisterUserRequest(
        email="test_user@example.com",
        password="A_Strong_Password123!",
    )
    try:
        result = register_user(user_request)
        print(f"User registered successfully: {result}")
    except RuntimeError as e:
        print(f"Error: {e}")
