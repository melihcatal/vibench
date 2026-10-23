from model_client import stream_text
from model_models import normalize_stream_chunk


def stream_completion(payload, config=None):
    prompt = payload["prompt"]
    return [normalize_stream_chunk(chunk) for chunk in stream_text(prompt, config=config)]
