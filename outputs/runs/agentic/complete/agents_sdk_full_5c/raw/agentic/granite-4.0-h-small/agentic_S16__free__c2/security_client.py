import os

class SecretManagerClient:
    """Generic wrapper that delegates to a concrete provider."""
    def __init__(self, provider=None):
        # Provider defaults selected per use case below
        if provider == 'aws':
            from secretmanager_aws import AwsSecretManager
            self.backend = AwsSecretManager()
        elif provider == 'azure':
            from secretmanager_azure import AzureKeyVault
            self.backend = AzureKeyVault()
        elif provider == 'gcp':
            from secretmanager_gcp import GcpSecretManager
            self.backend = GcpSecretManager()
        else:
            # default to GCP if no provider specified
            from secretmanager_gcp import GcpSecretManager
            self.backend = GcpSecretManager()
    
    def get_secret(self, name):
        """Retrieve the latest version of a secret."""
        return self.backend.get_secret(name)
    
    def get_secret_version(self, name, version):
        """Retrieve a specific version of a secret."""
        return self.backend.get_secret_version(name, version)

# Simple local implementations for demo purposes (could be replaced by real SDKs)
# In practice you would import the official provider SDKs.
if False:  # replace with real imports as needed
    from google.cloud import secretmanager as gcp_sm
    from boto3 import client as aws_client
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    
    class GcpSecretManager:
        def get_secret(self, name):
            # placeholder
            return 'secret_value'
        def get_secret_version(self, name, version):
            return 'version_value'
    
    class AwsSecretManager:
        def get_secret(self, name):
            return 'aws_secret_value'
        def get_secret_version(self, name, version):
            return 'aws_version_value'
    
    class AzureKeyVault:
        def get_secret(self, name):
            return 'azure_secret_value'
        def get_secret_version(self, name, version):
            return 'azure_version_value'
