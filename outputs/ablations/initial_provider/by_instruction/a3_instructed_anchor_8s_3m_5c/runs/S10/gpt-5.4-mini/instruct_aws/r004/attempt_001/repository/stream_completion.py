import json

from model_client import bedrock_runtime_client, get_config
from model_models import TextRequest


DEFAULT_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def stream_completion(request: TextRequest):
    config = get_config(DEFAULT_MODEL_ID)
    client = bedrock_runtime_client(config.region)
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "top_p": config.top_p,
        "messages": [{"role": "user", "content": [{"type": "text", "text": request.text}]}],
    }
    response = client.invoke_model_with_response_stream(modelId=config.model_id, body=json.dumps(payload))
    for event in response.get("body", []):
        chunk = event.get("chunk") if isinstance(event, dict) else None
        if not chunk:
            continue
        data = json.loads(chunk.get("bytes").decode("utf-8"))
        for part in data.get("content", []):
            if isinstance(part, dict) and part.get("type") == "text":
                yield part.get("text", "")
