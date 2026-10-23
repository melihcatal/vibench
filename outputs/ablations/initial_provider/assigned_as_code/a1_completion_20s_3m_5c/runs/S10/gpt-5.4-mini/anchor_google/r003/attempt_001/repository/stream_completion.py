from model_client import client_from_config, get_model_name


def stream_completion(payload, config=None):
    config = config or {}
    prompt = payload["prompt"]
    chunks = []
    with client_from_config(config) as client:
        for response in client.models.generate_content_stream(model=get_model_name(config), contents=prompt):
            if response.text:
                chunks.append(response.text)
    return {"text": "".join(chunks)}
