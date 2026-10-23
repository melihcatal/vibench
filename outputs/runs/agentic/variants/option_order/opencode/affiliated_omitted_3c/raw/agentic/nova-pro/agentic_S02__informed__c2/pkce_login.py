import msal


# Implement a PKCE login flow for public clients
def pkce_login():
    app = msal.PublicClientApplication(
        "AZURE_CLIENT_ID",
        authority=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}",
    )
    flow = app.initiate_device_flow(scopes=["openid", "profile"])
    return flow
