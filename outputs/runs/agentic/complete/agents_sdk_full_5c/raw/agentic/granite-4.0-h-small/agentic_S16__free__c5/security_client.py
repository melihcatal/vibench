# [HELPER] security_client.py
import os

class SecretManagerClient:
    """Thin wrapper that delegates to a concrete secret manager depending on configuration."""
    def __init__(self, provider=None):
        # Default to Google Cloud Secret Manager if no provider is specified
        self.provider = provider or os.getenv('SECRET_PROVIDER', 'gcp')
        if self.provider == 'gcp':
            from google.cloud import secretmanager
            self.client = secretmanager.SecretManagerServiceClient()
        elif self.provider == 'azure':
            from azure.keyvault.secrets import SecretClient
            vault_url = os.getenv('AZURE_KEYVAULT_URI')
            credential = os.getenv('AZURE_CLIENT_SECRET')  # placeholder; use proper auth in production
            self.client = SecretClient(vault_url=vault_url, credential=credential)
        elif self.provider == 'aws':
            import boto3
            self.client = boto3.client('secretsmanager')
        elif self.provider == 'hashicorp':
            from hvac import Client
            vault_addr = os.getenv('VAULT_ADDR')
            vault_token = os.getenv('VAULT_TOKEN')
            self.client = Client(url=vault_addr, token=vault_token)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def get_secret(self, name):
        """Generic method to fetch a secret value (bytes) from the configured provider."""
        if self.provider == 'gcp':
            response = self.client.access_secret_version(name=name)
            return response.payload.data
        elif self.provider == 'azure':
            return self.client.get_secret(name).value
        elif self.provider == 'aws':
            return self.client.get_secret_value(SecretId=name)['SecretString']
        elif self.provider == 'hashicorp':
            # Reads the latest version; callers handle versioning if needed
            secrets = self.client.secrets.kv.v2.read_secret_version(path=name)
            return secrets['data']['data']
        else:
            raise RuntimeError(f"Unsupported provider: {self.provider}")

    def read_secret_version(self, name, version_id):
        """Vault-specific helper for reading a particular version or staged value."""
        if self.provider != 'hashicorp':
            raise RuntimeError("read_secret_version only supported for HashiCorp Vault")
        if version_id.lower() == 'staged':
            response = self.client.secrets.kv.v2.read_secret_version(path=name, stage='staging')
            return response['data']['data']
        else:
            response = self.client.secrets.kv.v2.read_secret_version(path=name, version=version_id)
            return response['data']['data']
