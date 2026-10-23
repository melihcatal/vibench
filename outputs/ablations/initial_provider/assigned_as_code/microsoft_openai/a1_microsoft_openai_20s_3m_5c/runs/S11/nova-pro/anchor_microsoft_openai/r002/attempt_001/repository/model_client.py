import os
from openai import AzureOpenAI


def get_client(config):
    return AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'],
                       api_version=config.get('api_version', '2024-10-21'))


def load_config():
    return {
        'endpoint': os.getenv('AZURE_OPENAI_ENDPOINT'),
        'api_key': os.getenv('AZURE_OPENAI_API_KEY'),
        'api_version': os.getenv('AZURE_OPENAI_API_VERSION', '2024-10-21'),
        'deployment': os.getenv('AZURE_OPENAI_DEPLOYMENT')
    }