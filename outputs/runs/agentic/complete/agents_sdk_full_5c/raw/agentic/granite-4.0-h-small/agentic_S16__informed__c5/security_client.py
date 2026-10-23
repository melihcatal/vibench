import json

class SecretConfig:
    """Local helper for loading secret manager configuration."""
    def __init__(self, provider: str, **kwargs):
        self.provider = provider
        self.config = kwargs
        # Example: initialize SDK client based on provider
        if provider == 'aws':
            self.client = boto3.client('secretsmanager')
        elif provider == 'gcp':
            from google.cloud import secretmanager
            self.client = secretmanager.SecretManagerServiceClient()
        else:
            raise ValueError(f"Unsupported provider {provider}")

def get_config(provider: str, **kwargs):
    return SecretConfig(provider, **kwargs)
