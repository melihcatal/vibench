from model_client import get_platform_client

def collect_platform_metadata(input_text):
    client = get_platform_client()
    response = client.invoke_model(input_text=input_text)
    metadata = client.get_metadata(response)
    return response, metadata