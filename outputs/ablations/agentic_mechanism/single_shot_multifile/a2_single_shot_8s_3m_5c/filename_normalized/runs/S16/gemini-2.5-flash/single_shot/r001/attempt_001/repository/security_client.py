import os
import boto3
from google.cloud import secretmanager
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import hvac
from datadog_api_client.v2 import ApiClient, Configuration
from azure.cognitiveservices.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials
import openai
import deepl

class SecurityClients:
    _aws_secrets_manager_client = None
    _google_secret_manager_client = None
    _azure_key_vault_secret_client = None
    _hashicorp_vault_client = None
    _datadog_api_client = None
    _azure_content_moderator_client = None
    _openai_client = None
    _deepl_translator = None

    @classmethod
    def get_aws_secrets_manager_client(cls):
        if cls._aws_secrets_manager_client is None:
            cls._aws_secrets_manager_client = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION"))
        return cls._aws_secrets_manager_client

    @classmethod
    def get_google_secret_manager_client(cls):
        if cls._google_secret_manager_client is None:
            cls._google_secret_manager_client = secretmanager.SecretManagerServiceClient()
        return cls._google_secret_manager_client

    @classmethod
    def get_azure_key_vault_secret_client(cls):
        if cls._azure_key_vault_secret_client is None:
            vault_url = os.getenv("AZURE_KEY_VAULT_URL")
            if not vault_url:
                raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")
            credential = DefaultAzureCredential()
            cls._azure_key_vault_secret_client = SecretClient(vault_url=vault_url, credential=credential)
        return cls._azure_key_vault_secret_client

    @classmethod
    def get_hashicorp_vault_client(cls):
        if cls._hashicorp_vault_client is None:
            vault_addr = os.getenv("VAULT_ADDR")
            vault_token = os.getenv("VAULT_TOKEN")
            if not vault_addr or not vault_token:
                raise ValueError("VAULT_ADDR and VAULT_TOKEN environment variables must be set for HashiCorp Vault.")
            cls._hashicorp_vault_client = hvac.Client(url=vault_addr, token=vault_token)
            if not cls._hashicorp_vault_client.is_authenticated():
                raise ConnectionRefusedError("HashiCorp Vault client could not authenticate.")
        return cls._hashicorp_vault_client

    @classmethod
    def get_datadog_api_client(cls):
        if cls._datadog_api_client is None:
            configuration = Configuration()
            configuration.api_key["appKey"] = os.getenv("DATADOG_APPLICATION_KEY")
            configuration.api_key["apiKeyAuth"] = os.getenv("DATADOG_API_KEY")
            configuration.host = os.getenv("DATADOG_HOST", "https://api.datadoghq.com")
            cls._datadog_api_client = ApiClient(configuration)
        return cls._datadog_api_client

    @classmethod
    def get_azure_content_moderator_client(cls):
        if cls._azure_content_moderator_client is None:
            cm_endpoint = os.getenv("AZURE_CONTENT_MODERATOR_ENDPOINT")
            cm_key = os.getenv("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")
            if not cm_endpoint or not cm_key:
                raise ValueError("AZURE_CONTENT_MODERATOR_ENDPOINT and AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY environment variables must be set.")
            cls._azure_content_moderator_client = ContentModeratorClient(
                endpoint=cm_endpoint,
                credentials=CognitiveServicesCredentials(cm_key)
            )
        return cls._azure_content_moderator_client

    @classmethod
    def get_openai_client(cls):
        if cls._openai_client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set.")
            cls._openai_client = openai.OpenAI(api_key=api_key)
        return cls._openai_client

    @classmethod
    def get_deepl_translator(cls):
        if cls._deepl_translator is None:
            auth_key = os.getenv("DEEPL_AUTH_KEY")
            if not auth_key:
                raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
            cls._deepl_translator = deepl.Translator(auth_key)
        return cls._deepl_translator
