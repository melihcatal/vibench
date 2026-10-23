import os
import msal
from identity_models import UserCredentials, TokenResponse

def email_password_login(credentials: UserCredentials):
    # NOTE: Resource Owner Password Credentials (ROPC) flow is generally not recommended
    # for new applications due to security implications and lack of MFA support.
    # It also requires enabling ROPC in Azure AD tenant.
    # For typical user authentication, interactive flows with redirects (e.g., Authorization Code Flow)
    # or Azure AD B2C user flows are preferred.

    tenant_id = os.environ.get("MS_TENANT_ID")
    client_id = os.environ.get("MS_CLIENT_ID")
    client_secret = os.environ.get("MS_CLIENT_SECRET")

    if not all([tenant_id, client_id, client_secret]):
        raise ValueError("Missing one or more Microsoft Graph environment variables: MS_TENANT_ID, MS_CLIENT_ID, MS_CLIENT_SECRET")

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id, authority=authority, client_credential=client_secret
    )

    # For ROPC, the scope should include 'User.Read' or other relevant scopes for user data access.
    # 'offline_access' is needed to get a refresh token.
    scopes = ["User.Read", "openid", "profile", "offline_access"]

    result = app.acquire_token_by_username_password(
        username=credentials.email, 
        password=credentials.password, 
        scopes=scopes
    )

    if "access_token" in result:
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result.get("refresh_token"),
            expires_in=result.get("expires_in", 3600),  # Default to 1 hour if not provided
            token_type=result.get("token_type", "Bearer")
        )
    else:
        raise RuntimeError(f"Login failed: {result.get("error_description", result.get("error"))}")
