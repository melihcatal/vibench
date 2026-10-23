import msal
import uuid

AZURE_TENANT_ID = "your-tenant-id"
AZURE_CLIENT_ID = "your-client-id"


def pkce_login():
    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    app = msal.PublicClientApplication(AZURE_CLIENT_ID, authority=authority)
    code_verifier = uuid.uuid4()
    code_challenge = msal.create_code_challenge(code_verifier)
    login_uri = app.get_authorization_request_url(
        ["openid", "profile", "email"],
        redirect_uri="https://localhost",
        scopes=["user.read"],
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    print(f"Please visit this URL to authorize: {login_uri}")
    # Handle the callback and exchange code for tokens


if __name__ == "__main__":
    pkce_login()
