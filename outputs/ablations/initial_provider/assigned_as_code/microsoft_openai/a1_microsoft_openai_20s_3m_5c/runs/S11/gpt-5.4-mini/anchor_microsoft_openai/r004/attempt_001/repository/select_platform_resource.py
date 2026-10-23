from openai import AzureOpenAI


def select_platform_resource(payload, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'], api_version=config.get('api_version', '2024-10-21')) as client:
        models = client.models.list()
    target = payload.get('preferred_model') or config.get('deployment')
    for model in models.data:
        if model.id == target:
            return {'resource_id': model.id, 'model': model.id}
    return {'resource_id': target, 'model': target}
