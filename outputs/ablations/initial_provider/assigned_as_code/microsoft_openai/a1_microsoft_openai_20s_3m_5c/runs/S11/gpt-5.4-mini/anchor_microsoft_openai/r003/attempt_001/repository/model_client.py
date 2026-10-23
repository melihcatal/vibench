import os
from openai import AzureOpenAI


def load_platform_config(config=None):
    config = dict(config or {})
    config.setdefault('endpoint', os.environ['AZURE_OPENAI_ENDPOINT'])
    config.setdefault('api_key', os.environ['AZURE_OPENAI_API_KEY'])
    config.setdefault('api_version', os.environ.get('AZURE_OPENAI_API_VERSION', '2024-10-21'))
    config.setdefault('deployment', os.environ['AZURE_OPENAI_DEPLOYMENT'])
    return config


def build_platform_client(config=None):
    config = load_platform_config(config)
    return AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config['api_version'])
