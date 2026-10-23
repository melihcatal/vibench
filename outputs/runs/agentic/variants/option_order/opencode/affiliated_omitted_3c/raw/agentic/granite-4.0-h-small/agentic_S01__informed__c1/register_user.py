import os
import identity_client as client
import identity_models as models

# SAME-SCENARIO: register_user.py
# Creates a new email/password user account using Auth0 Management API


def register_user(payload: models.CreateUserRequest) -> models.CreateUserResponse:
    """Register a new user via the provider.  Returns the server's user record."""
    # Provider: Auth0 Management API (https://auth0.com/docs/api/management/v2)
    # Required env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
    url = f"https://{os.getenv('AUTH0_DOMAIN')}/api/v2/users"
    headers = {
        "Authorization": f"Bearer {os.getenv('AUTH0_CLIENT_SECRET')}",
        "Content-Type": "application/json",
    }
    response = client.get_auth0_client().post(url, json=payload.dict(), headers=headers)
    response.raise_for_status()
    data = response.json()
    # Map Auth0 response fields to our model
    return models.CreateUserResponse(
        user_id=data["user_id"], email=data["email"], created_at=data["created_at"]
    )


# Example (uncomment to test with real credentials)
# if __name__ == "__main__":
#     req = models.CreateUserRequest(email="jane.doe@example.com", password="SecurePass123")
#     print(register_user(req))
