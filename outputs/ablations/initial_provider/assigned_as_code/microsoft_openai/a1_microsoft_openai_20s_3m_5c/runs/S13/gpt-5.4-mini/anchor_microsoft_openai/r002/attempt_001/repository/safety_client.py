import os
from typing import Dict

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def load_safety_config(config: Dict = None) -> Dict:
    config = config or {}
    return {
        'endpoint': config.get('endpoint') or os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT'),
        'api_key': config.get('api_key') or os.environ.get('AZURE_CONTENT_SAFETY_KEY'),
    }


def get_client(config: Dict = None) -> ContentSafetyClient:
    cfg = load_safety_config(config)
    return ContentSafetyClient(cfg['endpoint'], AzureKeyCredential(cfg['api_key']))
