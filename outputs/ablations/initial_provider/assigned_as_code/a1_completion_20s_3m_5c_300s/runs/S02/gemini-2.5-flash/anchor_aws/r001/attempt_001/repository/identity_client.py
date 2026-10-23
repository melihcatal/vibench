import os

class IdentityClientConfig:
    def __init__(self,
                 domain_prefix=None,
                 region=None,
                 client_id=None,
                 client_secret=None,
                 identity_provider=None):
        self.domain_prefix = domain_prefix or os.environ.get("COGNITO_DOMAIN_PREFIX")
        self.region = region or os.environ.get("COGNITO_REGION", "us-east-1")
        self.client_id = client_id or os.environ.get("COGNITO_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("COGNITO_CLIENT_SECRET")
        self.identity_provider = identity_provider or os.environ.get("COGNITO_IDENTITY_PROVIDER")

    def to_dict(self):
        return {
            "domain_prefix": self.domain_prefix,
            "region": self.region,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "identity_provider": self.identity_provider
        }

def get_cognito_config(extra_config=None):
    config = IdentityClientConfig()
    if extra_config:
        for key, value in extra_config.items():
            setattr(config, key, value)
    return config.to_dict()
