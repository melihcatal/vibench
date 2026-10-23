from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import boto3
import google.cloud.secretmanager_v1beta1 as secretmanager
import hvac
import os

def get_azure_key_vault_secret_client(vault_url: str) -> SecretClient:
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)

def get_aws_secrets_manager_client():
    return boto3.client('secretsmanager')

def get_google_secret_manager_client():
    return secretmanager.SecretManagerServiceClient()

def get_hashicorp_vault_client(url: str, token: str):
    return hvac.Client(url=url, token=token)

def get_datadog_client():
    # Datadog API key and application key should be set as environment variables
    # DATADOG_API_KEY, DATADOG_APP_KEY
    # For simplicity, we'll just return a placeholder here.
    # In a real scenario, you'd initialize the Datadog API client.
    from datadog_api_client.v1 import ApiClient, Configuration
    from datadog_api_client.v1.api import MonitorsApi
    
    configuration = Configuration()
    # You might want to set these from environment variables
    configuration.api_key['apiKeyAuth'] = os.environ.get('DATADOG_API_KEY')
    configuration.api_key['appKeyAuth'] = os.environ.get('DATADOG_APP_KEY')
    
    return MonitorsApi(ApiClient(configuration))

def get_google_cloud_language_client():
    from google.cloud import language_v1
    return language_v1.LanguageServiceClient()

def get_openai_client():
    from openai import OpenAI
    return OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def get_google_cloud_translation_client():
    from google.cloud import translate
    return translate.TranslationServiceClient()
