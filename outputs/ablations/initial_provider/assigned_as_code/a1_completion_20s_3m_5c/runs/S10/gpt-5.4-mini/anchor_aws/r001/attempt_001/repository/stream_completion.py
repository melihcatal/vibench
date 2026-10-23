from model_client import get_bedrock_client, get_model_id
from model_models import normalize_text_payload, stream_bedrock_text


def stream_completion(payload, config=None):
    client = get_bedrock_client(config)
    response = client.converse_stream(
        modelId=get_model_id(config),
        messages=[{"role": "user", "content": [{"text": normalize_text_payload(payload)}]}],
    )
    text = ""
    for event in response.get("stream", []):
        text += stream_bedrock_text(event)
    return {"text": text}
