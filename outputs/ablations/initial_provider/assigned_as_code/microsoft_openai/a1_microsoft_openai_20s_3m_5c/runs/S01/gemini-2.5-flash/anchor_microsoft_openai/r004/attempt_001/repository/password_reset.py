import requests
from identity_client import IdentityClient
from identity_models import PasswordResetPayload

def password_reset(payload: PasswordResetPayload):
    identity_client = IdentityClient()
    access_token = identity_client.get_access_token()
    graph_api_base_url = identity_client.graph_api_base_url

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # First, find the user by email
    user_search_url = f"{graph_api_base_url}/users?$filter=identities/any(id:id/issuerAssignedId eq '{payload.email}' and id/signInType eq 'emailAddress')"
    search_response = requests.get(user_search_url, headers=headers, timeout=30)
    search_response.raise_for_status()
    search_results = search_response.json()

    if not search_results["value"]:
        raise ValueError(f"User with email {payload.email} not found.")

    user_id = search_results["value"][0]["id"]

    # To initiate a password reset, typically an admin would update the user's password.
    # For a self-service flow, Azure AD B2C is usually used.
    # Here, we'll simulate an admin-initiated password reset by generating a new password
    # and updating the user's password profile.
    # In a real scenario, this would involve a secure temporary password generation
    # and communication to the user, or directing them to a self-service portal.

    # For demonstration, we'll generate a placeholder new password.
    # IMPORTANT: In a production system, securely generate and handle new passwords.
    new_password = "TempPass!123"

    update_password_url = f"{graph_api_base_url}/users/{user_id}"
    update_data = {
        "passwordProfile": {
            "password": new_password,
            "forceChangePasswordNextSignIn": True
        }
    }

    update_response = requests.patch(update_password_url, headers=headers, json=update_data, timeout=30)
    update_response.raise_for_status()

    return {"message": f"Password reset initiated for user {payload.email}. User must change password on next sign-in."}
