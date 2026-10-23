from.model_client import ModelClient

def select_resource():
    client = ModelClient().get_client()
    return client.get_models()