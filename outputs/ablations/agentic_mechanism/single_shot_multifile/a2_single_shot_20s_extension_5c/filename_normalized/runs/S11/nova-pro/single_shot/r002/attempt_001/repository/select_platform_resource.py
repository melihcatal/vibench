from model_client import get_platform_client

def select_platform_resource():
    client = get_platform_client()
    resource = client.select_model(model_id='text-davinci-003')
    return resource