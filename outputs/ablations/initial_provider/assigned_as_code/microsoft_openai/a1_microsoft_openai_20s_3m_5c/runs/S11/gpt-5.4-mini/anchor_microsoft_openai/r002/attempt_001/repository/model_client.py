import os
from openai import AzureOpenAI


def load_config(config=None):
    merged = dict(config or {})
    merged.setdefault('endpoint', os.environ.get('AZURE_OPENAI_ENDPOINT', ''))
    merged.setdefault('api_key', os.environ.get('AZURE_OPENAI_API_KEY', ''))
    merged.setdefault('api_version', os.environ.get('AZURE_OPENAI_API_VERSION', '2024-10-21'))
    merged.setdefault('deployment', os.environ.get('AZURE_OPENAI_DEPLOYMENT', ''))
    return merged


def build_client(config=None):
    config = load_config(config)
    return AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config['api_version'])
