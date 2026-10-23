import os
import boto3
import hvac
from google.cloud import secretmanager, dlp_v2, translate
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import openai

class SecretManagementClients:
    """Provides centralized client initialization for various secret management services."""

    @staticmethod
    def get_aws_secrets_manager_client():
        region_name = os.environ.get("AWS_REGION", "us-east-1")
        session = boto3.session.Session()
        return session.client(service_name='secretsmanager', region_name=region_name)

    @staticmethod
    def get_aws_config_client():
        region_name = os.environ.get("AWS_REGION", "us-east-1")
        session = boto3.session.Session()
        return session.client(service_name='config', region_name=region_name)

    @staticmethod
    def get_google_secret_manager_client():
        return secretmanager.SecretManagerServiceClient()

    @staticmethod
    def get_azure_key_vault_secret_client(vault_url: str):
        credential = DefaultAzureCredential()
        return SecretClient(vault_url=vault_url, credential=credential)

    @staticmethod
    def get_hashicorp_vault_client():
        vault_addr = os.environ.get("VAULT_ADDR")
        vault_token = os.environ.get("VAULT_TOKEN")
        if not vault_addr or not vault_token:
            raise ValueError("VAULT_ADDR and VAULT_TOKEN environment variables must be set for HashiCorp Vault.")
        return hvac.Client(url=vault_addr, token=vault_token)

    @staticmethod
    def get_google_dlp_client():
        return dlp_v2.DlpServiceClient()

    @staticmethod
    def get_openai_client():
        # OpenAI API key is usually picked up from OPENAI_API_KEY environment variable
        return openai.OpenAI()

    @staticmethod
    def get_google_translate_client():
        return translate.TranslationServiceClient()
