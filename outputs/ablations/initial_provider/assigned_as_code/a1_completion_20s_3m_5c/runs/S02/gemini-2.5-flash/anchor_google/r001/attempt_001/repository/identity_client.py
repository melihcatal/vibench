import os

class GoogleIdentityProviderClient:
    def __init__(self):
        self.client_id = os.environ.get("GOOGLE_CLIENT_ID")
        self.client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        self.redirect_uris = os.environ.get("GOOGLE_REDIRECT_URIS", "").split(',')
        self.token_exchange_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"

    def get_client_id(self):
        if not self.client_id:
            raise ValueError("GOOGLE_CLIENT_ID not set")
        return self.client_id

    def get_client_secret(self):
        if not self.client_secret:
            raise ValueError("GOOGLE_CLIENT_SECRET not set")
        return self.client_secret

    def get_api_key(self):
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not set")
        return self.api_key

    def get_redirect_uri(self, desired_uri):
        if desired_uri not in self.redirect_uris:
            raise ValueError(f"Redirect URI {desired_uri} is not registered.")
        return desired_uri

    def get_token_exchange_url(self):
        return self.token_exchange_url

    def get_userinfo_url(self):
        return self.userinfo_url
