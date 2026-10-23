import os
import identity_client as client
import identity_models as models

# SAME-SCENARIO: password_reset.py
# Starts a password reset flow for a local account


def initiate_password_reset(email: str):
    """Trigger a password reset email for the given email address."""
    # Provider: Auth0 Management API (https://auth0.com/docs/api/management/v2)
    # Required env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
    url = f"https://{os.getenv('AUTH0_DOMAIN')}/api/v2/tickets/password-change"
    payload = {"email": email, "connection": "Username-Password-Authentication"}
    headers = {
        "Authorization": f"Bearer {os.getenv('AUTH0_CLIENT_SECRET')}",
        "Content-Type": "application/json",
    }
    resp = client.get_auth0_client().post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return models.PasswordResetResponse(
        request_id=data["request_id"], message=data["message"]
    )


# Example (uncomment)
# if __name__ == "__main__":
#     result = initiate_password_reset("user@example.com")
#     print(result)
