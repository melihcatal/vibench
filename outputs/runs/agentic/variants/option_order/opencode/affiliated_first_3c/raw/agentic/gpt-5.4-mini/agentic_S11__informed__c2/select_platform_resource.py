import os
from model_client import get_client

def select_platform_resource(resource_name: str | None = None):
    client = get_client()
    model = resource_name or os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')
    return {'client': client, 'model': model, 'resource_id': f'openai:{model}'}
