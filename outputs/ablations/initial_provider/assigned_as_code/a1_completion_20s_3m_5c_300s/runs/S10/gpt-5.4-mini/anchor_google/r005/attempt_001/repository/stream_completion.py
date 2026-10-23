from model_client import build_prompt, create_client, get_model
from model_models import normalize_stream_chunk


def stream_completion(payload, config=None):
    config = config or {}
    prompt = build_prompt(payload["prompt"])
    with create_client(config) as client:
        stream = client.models.generate_content_stream(model=get_model(config), contents=prompt)
        return [normalize_stream_chunk(chunk) for chunk in stream]
