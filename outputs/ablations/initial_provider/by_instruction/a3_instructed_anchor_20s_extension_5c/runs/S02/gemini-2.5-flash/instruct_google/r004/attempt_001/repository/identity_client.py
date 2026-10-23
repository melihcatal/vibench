import os

class IdentityClientConfig:
    def __init__(self):
        self.google_client_id = os.environ.get("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        self.google_auth_uri = "https://accounts.google.com/o/oauth2/auth"
        self.google_token_uri = "https://oauth2.googleapis.com/token"
        self.google_userinfo_uri = "https://openidconnect.googleapis.com/v1/userinfo"
        self.google_redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5000/oauth2callback")
        self.google_pkce_redirect_uri = os.environ.get("GOOGLE_PKCE_REDIRECT_URI", "http://localhost:5000/pkce_callback")
        self.google_scopes = [
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ]

class IdentityClient:
    def __init__(self):
        self.config = IdentityClientConfig()

    def get_google_oauth_config(self):
        return {
            "client_id": self.config.google_client_id,
            "client_secret": self.config.google_client_secret,
            "auth_uri": self.config.google_auth_uri,
            "token_uri": self.config.google_token_uri,
            "userinfo_uri": self.config.google_userinfo_uri,
            "redirect_uris": [self.config.google_redirect_uri],
            "scopes": self.config.google_scopes,
        }

if __name__ == "__main__":
    client = IdentityClient()
    print("Google OAuth Configuration:")
    print(client.get_google_oauth_config())
