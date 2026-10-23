import os


class Auth0Config:
    DOMAIN = os.environ.get("AUTH0_DOMAIN", "your-auth0-domain.auth0.com")
    CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "your_auth0_client_id")
    CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "your_auth0_client_secret")
    CALLBACK_URL = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
    )
    AUDIENCE = os.environ.get("AUTH0_AUDIENCE", f"https://{{DOMAIN}}/api/v2/")

    AUTHORIZE_URL = f"https://{{DOMAIN}}/authorize"
    TOKEN_URL = f"https://{{DOMAIN}}/oauth/token"
    USERINFO_URL = f"https://{{DOMAIN}}/userinfo"

    # For PKCE
    PKCE_CHALLENGE_METHOD = "S256"
