from openai import AzureOpenAI


def select_platform_resource(config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        deployment = config.get('deployment') or client.models.list().data[0].id
    return {'deployment': deployment}
