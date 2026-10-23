import os

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def safety_config(config=None):
    config = config or {}
    return {
        'endpoint': config.get('endpoint', os.environ['AZURE_CONTENT_SAFETY_ENDPOINT']),
        'api_key': config.get('api_key', os.environ['AZURE_CONTENT_SAFETY_KEY']),
    }


def create_client(config=None):
    cfg = safety_config(config)
    return ContentSafetyClient(cfg['endpoint'], AzureKeyCredential(cfg['api_key']))
