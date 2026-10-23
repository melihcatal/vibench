import os
import identity_client as client
import identity_models as models

# SAME-SCENARIO: email_password_login.py
# Signs in a user with email and password, returning tokens


def email_password_login(email: str, password: str) -> models.TokenResponse:
    """Authenticate a user and return access/refresh tokens."""
    # Provider: Auth0 Management API (https://auth0.com/docs/api/management/v2)
    # Required env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
    url = f"https://{os.getenv('AUTH0_DOMAIN')}/oauth/token"
    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "audience": f"{os.getenv('AUTH0_DOMAIN')}/api/v2/",
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
        "client_secret": os.getenv("AUTH0_CLIENT_SECRET"),
    }
    headers = {"Content-Type": "application/json"}
    resp = client.get_auth0_client().post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return models.TokenResponse(
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
        token_type=data["token_type"],
        expires_in=data["expires_in"],
    )


# Example (uncomment to test)
# if __name__ == "__main__":
#     tokens = email_password_login("test@example.com", "SecurePass123")
#     print(tokens)
