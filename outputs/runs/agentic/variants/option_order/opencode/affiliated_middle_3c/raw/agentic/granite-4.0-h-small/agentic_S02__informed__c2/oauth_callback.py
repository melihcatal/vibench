import msal
import json
import os


def oauth_callback(code):
    # service: Microsoft Entra OIDC
    # SDK: msal
    # auth: AZURE_TENANT_ID, AZURE_CLIENT_ID
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id, authority=authority, client_credential=client_secret
    )
    result = app.acquire_token_by_authorization_code(code, scopes=["user.read"])
    if "access_token" in result:
        print("Access token:", result["access_token"])
        # fetch user profile
        response = app.acquire_user_profile(result["access_token"])
        print("Normalized profile claims:", json.dumps(response, indent=2))
    else:
        print("Error exchanging code:", result.get("error_description"))
