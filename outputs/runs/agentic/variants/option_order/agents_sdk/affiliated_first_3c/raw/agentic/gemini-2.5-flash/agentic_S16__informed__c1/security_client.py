import os
import boto3
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from google.cloud import secretmanager
from ibm_secrets_manager_sdk.secrets_manager_v1 import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class SecurityClient:
    """
    Provides initialized clients for various secret management services.
    """

    def get_aws_secrets_manager_client(self):
        """Returns a configured boto3 Secrets Manager client."""
        region = os.environ.get('AWS_REGION', 'us-east-1')
        return boto3.client('secretsmanager', region_name=region)

    def get_azure_key_vault_client(self):
        """Returns a configured Azure Key Vault Secrets client."""
        key_vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
        if not key_vault_url:
            raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")
        credential = DefaultAzureCredential()
        return SecretClient(vault_url=key_vault_url, credential=credential)

    def get_google_secret_manager_client(self):
        """Returns a configured Google Secret Manager client."""
        return secretmanager.SecretManagerServiceClient()

    def get_ibm_secrets_manager_client(self):
        """Returns a configured IBM Cloud Secrets Manager client."""
        api_key = os.environ.get("IBM_SECRETS_MANAGER_APIKEY")
        service_url = os.environ.get("IBM_SECRETS_MANAGER_SERVICE_URL")
        if not api_key or not service_url:
            raise ValueError("IBM_SECRETS_MANAGER_APIKEY and IBM_SECRETS_MANAGER_SERVICE_URL environment variables must be set.")
        authenticator = IAMAuthenticator(api_key)
        service = SecretsManagerV1(authenticator=authenticator)
        service.set_service_url(service_url)
        return service

# Example usage (not scored, for local testing):
if __name__ == '__main__':
    client_helper = SecurityClient()
    print("SecurityClient initialized.")
    # You would typically use these clients within your integration files,
    # rather than instantiating them directly here.
    # try:
    #     aws_client = client_helper.get_aws_secrets_manager_client()
    #     print("AWS Secrets Manager client obtained.")
    # except Exception as e:
    #     print(f"Could not get AWS client: {e}")

    # try:
    #     azure_client = client_helper.get_azure_key_vault_client()
    #     print("Azure Key Vault client obtained.")
    # except Exception as e:
    #     print(f"Could not get Azure client: {e}")
