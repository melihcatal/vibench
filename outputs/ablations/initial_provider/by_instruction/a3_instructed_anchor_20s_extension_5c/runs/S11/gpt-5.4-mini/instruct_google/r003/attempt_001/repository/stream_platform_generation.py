from model_client import create_client, load_platform_config
from model_models import normalize_text


def stream_platform_generation(prompt: str):
    config = load_platform_config()
    client = create_client()
    stream = client.models.generate_content_stream(model=config.model, contents=prompt)
    for chunk in stream:
        yield {"chunk": chunk, "text": normalize_text(getattr(chunk, "text", chunk))}
