from openai import AzureOpenAI


def select_platform_resource(config):
    client = AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21'))
    response = client.models.list()
    for model in response.data:
        if model.id == config['deployment']:
            return model
    return None