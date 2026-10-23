from google import genai

from model_client import get_api_key, get_model


def stream_completion(payload, config=None):
    config = config or {}
    prompt = payload["prompt"]
    chunks = []
    with genai.Client(api_key=get_api_key(config)) as client:
        for chunk in client.models.generate_content_stream(model=get_model(config), contents=prompt):
            text = getattr(chunk, "text", "") or ""
            if text:
                chunks.append(text)
    return {"text": "".join(chunks)}
