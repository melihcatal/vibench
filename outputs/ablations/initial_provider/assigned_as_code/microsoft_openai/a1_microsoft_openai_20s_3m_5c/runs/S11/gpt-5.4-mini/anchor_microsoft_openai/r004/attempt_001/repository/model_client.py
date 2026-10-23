import os
from openai import AzureOpenAI


def load_platform_config(overrides=None):
    config = {
        'endpoint': os.environ.get('AZURE_OPENAI_ENDPOINT', ''),
        'api_key': os.environ.get('AZURE_OPENAI_API_KEY', ''),
        'api_version': os.environ.get('AZURE_OPENAI_API_VERSION', '2024-10-21'),
        'deployment': os.environ.get('AZURE_OPENAI_DEPLOYMENT', ''),
    }
    if overrides:
        config.update(overrides)
    return config


def create_platform_client(config=None):
    config = load_platform_config(config)
    return AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config['api_version'])
