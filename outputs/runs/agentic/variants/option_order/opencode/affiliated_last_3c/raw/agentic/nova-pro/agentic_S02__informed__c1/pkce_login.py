import msal

AZURE_TENANT_ID = "your_tenant_id"
AZURE_CLIENT_ID = "your_client_id"


def pkce_login():
    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    client = msal.PublicClientApplication(AZURE_CLIENT_ID, authority=authority)
    code_verifier = msal.create_code_verifier()
    code_challenge = msal.create_code_challenge(code_verifier)
    login_url = client.get_authorization_request_url(
        ["openid", "profile", "email"],
        redirect_uri="http://localhost:5000/oauth_callback",
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    print(f"Please navigate to {login_url} to start the login process")
