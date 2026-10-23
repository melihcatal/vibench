from model_client import get_platform_client

def select_platform_resource():
    client = get_platform_client()
    models = client.models.list()
    for model in models.data:
        if "gpt" in model.id.lower():
            return model.id
    return models.data[0].id if models.data else None
