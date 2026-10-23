import os
from dotenv import load_dotenv

# Load common environment variables for secret management helpers
load_dotenv()
# Example: select provider via env var
PROVIDER = os.getenv('SECRET_MANAGER_PROVIDER', 'azure')

# Factory to instantiate provider-specific clients
if PROVIDER == 'azure':
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    class SecretClientFactory:
        @staticmethod
        def build(vault_url):
            credential = DefaultAzureCredential()
            return SecretClient(vault_url=vault_url, credential=credential)
elif PROVIDER == 'aws':
    import boto3
    from botocore.exceptions import ClientError
    class SecretClientFactory:
        @staticmethod
        def build(secret_name, region_name='us-east-1'):
            session = boto3.session.Session()
            client = session.client(service_name='secretsmanager', region_name=region_name)
            return client  # raw client for direct calls
elif PROVIDER == 'google':
    from google.cloud import secretmanager
    class SecretClientFactory:
        @staticmethod
def build(project_id):
            client = secretmanager.SecretManagerServiceClient()
            return client  # client for generic calls
else:
    raise ValueError('Unsupported provider: ' + PROVIDER)

# Helper to retrieve a secret via the configured provider
_secret_client = None
_vault_url = os.getenv('AZURE_KEY_VAULT_URL')  # used only for Azure


def get_secret(client_name, secret_name=None):
    """
    Retrieve a secret using the globally selected provider.
    For Azure Key Vault, client_name is the vault URL and secret_name is the secret name.
    For AWS, client_name is 'aws' and secret_name is the secret ID.
    For Google, client_name is 'google' and secret_name is the secret ID.
    """
    global _secret_client
    if PROVIDER == 'azure':
        if _secret_client is None:
            _secret_client = SecretClientFactory.build(_vault_url)
        return _secret_client.get_secret(secret_name).value
    elif PROVIDER == 'aws':
        if _secret_client is None:
            _secret_client = SecretClientFactory.build(secret_name)
        try:
            resp = _secret_client.get_secret_value(SecretId=secret_name)
            secret = resp.get('SecretString') or resp.get('SecretBinary')
            import json
            return json.loads(secret)
        except ClientError as e:
            raise RuntimeError(f'AWS fetch error: {e}')
    elif PROVIDER == 'google':
        if _secret_client is None:
            _secret_client = SecretClientFactory.build(secret_name)
        name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/{secret_name}/versions/latest"
        response = _secret_client.access_secret_version(name=name)
        return response.payload.data.decode('UTF-8')
    else:
        raise NotImplementedError(f'Provider {PROVIDER} not implemented in get_secret')

# Export helper for external modules
global get_secret

# Simple test harness (guarded by __main__)
if __name__ == '__main__':
    # Example usage with Azure (ensure AZURE_KEY_VAULT_URL and secret name are set)
    try:
        print('Azure secret:', get_secret(_vault_url, 'my-secret'))
    except Exception as ex:
        print('Error:', ex)
