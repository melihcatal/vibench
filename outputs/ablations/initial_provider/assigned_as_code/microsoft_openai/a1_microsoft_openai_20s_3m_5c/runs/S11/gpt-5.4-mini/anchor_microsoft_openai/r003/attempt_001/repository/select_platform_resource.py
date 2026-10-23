from openai import AzureOpenAI


def select_platform_resource(payload, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        resource = client.models.retrieve(config['deployment'])
    return {'resource_id': resource.id, 'model': resource.id, 'text': payload['text']}
