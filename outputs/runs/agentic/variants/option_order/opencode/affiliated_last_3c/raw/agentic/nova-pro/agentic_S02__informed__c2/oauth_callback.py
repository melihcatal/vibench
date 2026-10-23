import msal

AZURE_TENANT_ID = "your-tenant-id"
AZURE_CLIENT_ID = "your-client-id"


# Handle OAuth callback
def oauth_callback(auth_result):
    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    client = msal.PublicClientApplication(AZURE_CLIENT_ID, authority=authority)
    result = client.acquire_token_by_auth_code_flow(auth_result, auth_result["code"])
    if "access_token" in result:
        print("Access token acquired")
    else:
        print("Error acquiring token:", result.get("error"))
    return result
