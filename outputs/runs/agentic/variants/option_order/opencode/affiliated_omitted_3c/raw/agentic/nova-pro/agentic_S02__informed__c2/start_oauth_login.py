import msal


# Start an OAuth or OIDC authorization-code login
def start_oauth_login():
    app = msal.ConfidentialClientApplication(
        "AZURE_CLIENT_ID",
        authority=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}",
        client_credential={"client_secret": "AZURE_CLIENT_SECRET"},
    )
    flow = app.initiate_auth_code_flow(
        ["openid", "profile"], redirect_uri="https://localhost"
    )
    return flow["auth_uri"]
