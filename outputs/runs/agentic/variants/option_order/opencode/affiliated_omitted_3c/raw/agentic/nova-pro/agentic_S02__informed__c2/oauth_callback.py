import msal


# Handle the callback and exchange an authorization code for tokens
def oauth_callback(code):
    app = msal.ConfidentialClientApplication(
        "AZURE_CLIENT_ID",
        authority=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}",
        client_credential={"client_secret": "AZURE_CLIENT_SECRET"},
    )
    result = app.acquire_token_by_auth_code_flow(code, ["openid", "profile"])
    return result
