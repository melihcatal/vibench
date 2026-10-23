from openai import AzureOpenAI


def get_client(config):
    return AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21'))

