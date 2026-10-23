import msal

AZURE_TENANT_ID = "your-tenant-id"
AZURE_CLIENT_ID = "your-client-id"


def start_oauth_login():
    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    app = msal.PublicClientApplication(AZURE_CLIENT_ID, authority=authority)
    login_uri = app.get_authorization_request_url(
        ["openid", "profile", "email"],
        redirect_uri="https://localhost",
        scopes=["user.read"],
    )
    print(f"Please visit this URL to authorize: {login_uri}")


if __name__ == "__main__":
    start_oauth_login()
