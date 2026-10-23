import os
import requests
from identity_models import PasswordResetPayload, PasswordResetResponse
from identity_client import get_identity_client_from_env

MICROSOFT_GRAPH_API_URL = "https://graph.microsoft.com/v1.0"

def password_reset(payload: PasswordResetPayload) -> PasswordResetResponse:
    identity_client = get_identity_client_from_env()
    headers = identity_client.get_ms_graph_client_headers()

    # First, find the user by email address
    search_url = f"{MICROSOFT_GRAPH_API_URL}/users?$filter=identities/any(id:id/issuerAssignedId eq '{payload.email}' and id/issuer eq '{identity_client.issuer}')"
    # If issuer is not used, filter by userPrincipalName or other attributes
    # For simplicity, assuming userPrincipalName is the email or a similar identifier
    if not identity_client.issuer:
        search_url = f"{MICROSOFT_GRAPH_API_URL}/users?$filter=userPrincipalName eq '{payload.email}'"

    search_response = requests.get(search_url, headers=headers, timeout=30)
    search_response.raise_for_status()
    users = search_response.json().get('value', [])

    if not users:
        # For security reasons, it's generally better not to disclose if a user exists or not.
        # A generic success message is often preferred in real-world password reset flows.
        return PasswordResetResponse(message="If an account with that email exists, a password reset link has been sent.")

    user_id = users[0]['id']

    # In a real scenario, for self-service password reset with Azure AD, you'd typically
    # redirect the user to a Microsoft-hosted password reset page, or if using B2C, trigger a user flow.
    # Programmatically triggering an email for password reset via Graph API is not a direct feature for end-users.
    # However, an admin can force a user to change password at next sign-in.
    # This simulation forces a password change for the user by updating their password profile.
    # This requires `User.ReadWrite.All` or `Directory.AccessAsUser.All` permissions.

    update_url = f"{MICROSOFT_GRAPH_API_URL}/users/{user_id}"
    update_payload = {
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True
        }
    }

    update_response = requests.patch(update_url, headers=headers, json=update_payload, timeout=30)
    update_response.raise_for_status()

    return PasswordResetResponse(message=f"Password reset initiated for user {payload.email}. User will be prompted to change password on next sign-in.")
