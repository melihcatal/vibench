from model_client import get_client, get_model_name


def stream_platform_generation(prompt: str, model: str = None):
    client = get_client()
    model_name = model or get_model_name()
    return client.models.generate_content_stream(model=model_name, contents=prompt)
