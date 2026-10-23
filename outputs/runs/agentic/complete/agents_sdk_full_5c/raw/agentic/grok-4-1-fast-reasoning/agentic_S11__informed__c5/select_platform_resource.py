from model_client import get_client

def select_platform_resource(filter_pattern: str = 'gpt-4o') -> str:
    client = get_client()
    models_response = client.models.list()
    for model_data in models_response.data:
        if filter_pattern.lower() in model_data.id.lower():
            return model_data.id
    raise ValueError(f'No matching resource found for pattern: {filter_pattern}')
