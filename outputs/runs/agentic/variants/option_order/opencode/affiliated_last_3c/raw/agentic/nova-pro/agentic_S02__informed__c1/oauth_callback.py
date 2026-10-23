import msal

AZURE_TENANT_ID = "your_tenant_id"
AZURE_CLIENT_ID = "your_client_id"


def oauth_callback(auth_result):
    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    client = msal.PublicClientApplication(AZURE_CLIENT_ID, authority=authority)
    result = client.acquire_token_by_authorization_code(
        auth_result["code"],
        ["openid", "profile", "email"],
        redirect_uri="http://localhost:5000/oauth_callback",
    )
    print(result)
