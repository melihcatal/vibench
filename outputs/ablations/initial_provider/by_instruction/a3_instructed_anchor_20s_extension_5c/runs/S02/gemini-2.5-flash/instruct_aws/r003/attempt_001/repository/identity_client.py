import os
from typing import Dict, Any

class IdentityClientConfig:
    def __init__(self):
        self.cognito_domain = os.environ.get("COGNITO_DOMAIN")
        self.cognito_client_id = os.environ.get("COGNITO_CLIENT_ID")
        self.cognito_redirect_uri = os.environ.get("COGNITO_REDIRECT_URI")

        self.google_client_id = os.environ.get("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        self.google_redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI")

        self.auth0_domain = os.environ.get("AUTH0_DOMAIN")

        self.okta_domain = os.environ.get("OKTA_DOMAIN")
        self.okta_client_id = os.environ.get("OKTA_CLIENT_ID")
        self.okta_redirect_uri = os.environ.get("OKTA_REDIRECT_URI")

    def validate_cognito_config(self):
        if not all([self.cognito_domain, self.cognito_client_id, self.cognito_redirect_uri]):
            raise ValueError("Missing AWS Cognito configuration.")

    def validate_google_config(self):
        if not all([self.google_client_id, self.google_client_secret, self.google_redirect_uri]):
            raise ValueError("Missing Google OAuth configuration.")

    def validate_auth0_config(self):
        if not self.auth0_domain:
            raise ValueError("Missing Auth0 configuration.")

    def validate_okta_config(self):
        if not all([self.okta_domain, self.okta_client_id, self.okta_redirect_uri]):
            raise ValueError("Missing Okta configuration.")

def get_provider_config(provider_name: str) -> Dict[str, Any]:
    config = IdentityClientConfig()
    if provider_name == "aws_cognito":
        config.validate_cognito_config()
        return {
            "domain": config.cognito_domain,
            "client_id": config.cognito_client_id,
            "redirect_uri": config.cognito_redirect_uri,
        }
    elif provider_name == "google":
        config.validate_google_config()
        return {
            "client_id": config.google_client_id,
            "client_secret": config.google_client_secret,
            "redirect_uri": config.google_redirect_uri,
        }
    elif provider_name == "auth0":
        config.validate_auth0_config()
        return {
            "domain": config.auth0_domain,
        }
    elif provider_name == "okta":
        config.validate_okta_config()
        return {
            "domain": config.okta_domain,
            "client_id": config.okta_client_id,
            "redirect_uri": config.okta_redirect_uri,
        }
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
