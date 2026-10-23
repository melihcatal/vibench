import os

class GoogleOauthClientConfig:
    def __init__(self):
        self.client_id = os.environ.get("GOOGLE_CLIENT_ID")
        self.client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        self.redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI")
        self.authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        self.scopes = "openid email profile"

    def validate(self):
        if not self.client_id or not self.redirect_uri:
            raise ValueError("Google client ID and redirect URI must be set.")
        # Client secret is not always required for public clients (PKCE flow)
        # if not self.client_secret:
        #     raise ValueError("Google client secret must be set.")


def get_google_oauth_config():
    config = GoogleOauthClientConfig()
    config.validate()
    return config
