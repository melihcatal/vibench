import os

class IdentityClientConfig:
    def __init__(self):
        # Google OAuth Configuration
        self.google_client_id = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
        self.google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
        self.google_redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/oauth/callback/google")
        
        # Okta PKCE Configuration
        self.okta_org_url = os.environ.get("OKTA_ORG_URL", "https://{your-okta-domain}.okta.com")
        self.okta_client_id = os.environ.get("OKTA_CLIENT_ID", "YOUR_OKTA_CLIENT_ID")
        self.okta_redirect_uri = os.environ.get("OKTA_REDIRECT_URI", "http://localhost:8080/pkce/callback")
        self.okta_authz_server_id = os.environ.get("OKTA_AUTHZ_SERVER_ID", "default")

    def __repr__(self):
        return f"IdentityClientConfig(Google Client ID: {self.google_client_id}, Okta Org URL: {self.okta_org_url})"

def load_identity_config() -> IdentityClientConfig:
    """Loads and returns the identity client configuration."""
    return IdentityClientConfig()

if __name__ == "__main__":
    config = load_identity_config()
    print("Loaded Identity Configuration:")
    print(f"  Google Client ID: {config.google_client_id}")
    print(f"  Okta Org URL: {config.okta_org_url}")
