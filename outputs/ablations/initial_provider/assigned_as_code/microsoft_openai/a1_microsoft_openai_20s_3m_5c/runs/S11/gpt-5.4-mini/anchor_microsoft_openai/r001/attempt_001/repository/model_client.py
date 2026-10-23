import os
from openai import AzureOpenAI


def load_platform_config(overrides=None):
    overrides = overrides or {}
    return {
        'endpoint': overrides.get('endpoint', os.environ['AZURE_OPENAI_ENDPOINT']),
        'api_key': overrides.get('api_key', os.environ['AZURE_OPENAI_API_KEY']),
        'api_version': overrides.get('api_version', os.environ.get('AZURE_OPENAI_API_VERSION', '2024-10-21')),
        'deployment': overrides.get('deployment', os.environ['AZURE_OPENAI_DEPLOYMENT']),
    }


def create_platform_client(config):
    return AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config['api_version'])
