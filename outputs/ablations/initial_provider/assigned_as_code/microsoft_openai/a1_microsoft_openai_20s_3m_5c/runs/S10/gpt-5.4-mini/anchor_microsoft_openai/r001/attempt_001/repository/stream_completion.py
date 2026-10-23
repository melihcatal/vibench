from model_client import get_client, get_model
from model_models import text_from_payload, extract_stream_content


def stream_completion(payload, config=None):
    config = config or {}
    client = get_client(config)
    prompt = text_from_payload(payload)
    stream = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': prompt}], stream=True)
    parts = []
    for chunk in stream:
        part = extract_stream_content(chunk)
        if part:
            parts.append(part)
    return {'text': ''.join(parts)}
