import msal

AZURE_TENANT_ID = "your-tenant-id"
AZURE_CLIENT_ID = "your-client-id"


def oauth_callback(code):
    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    app = msal.PublicClientApplication(AZURE_CLIENT_ID, authority=authority)
    token_response = app.acquire_token_by_authorization_code(
        code, scopes=["user.read"], redirect_uri="https://localhost"
    )
    print(token_response)


if __name__ == "__main__":
    oauth_callback("your-authorization-code")
