from model_client import get_platform_client

def stream_platform_generation(input_text):
    client = get_platform_client()
    for response in client.stream_model(input_text=input_text):
        yield response