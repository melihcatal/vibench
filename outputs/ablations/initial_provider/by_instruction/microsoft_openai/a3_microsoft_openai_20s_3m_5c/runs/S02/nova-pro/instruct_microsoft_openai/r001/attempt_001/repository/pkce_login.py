import msal

def pkce_login():
    app = msal.PublicClientApplication(
        client_id="your-client-id",
        authority="https://login.microsoftonline.com/your-tenant-id",
        client_credential="your-client-secret"
    )
    flow = app.initiate_auth_code_flow(
        scopes=["user.read"],
        redirect_uri="https://your-redirect-uri",
        code_challenge_method="S256"
    )
    print(f"Please go to the following URL to log in: {flow['auth_uri']}")
    return flow['state']