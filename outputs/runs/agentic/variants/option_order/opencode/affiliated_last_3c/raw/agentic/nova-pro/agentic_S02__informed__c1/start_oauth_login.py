import msal

AZURE_TENANT_ID = "your_tenant_id"
AZURE_CLIENT_ID = "your_client_id"


def start_oauth_login():
    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    client = msal.PublicClientApplication(AZURE_CLIENT_ID, authority=authority)
    login_url = client.get_authorization_request_url(
        ["openid", "profile", "email"],
        redirect_uri="http://localhost:5000/oauth_callback",
    )
    print(f"Please navigate to {login_url} to start the login process")
