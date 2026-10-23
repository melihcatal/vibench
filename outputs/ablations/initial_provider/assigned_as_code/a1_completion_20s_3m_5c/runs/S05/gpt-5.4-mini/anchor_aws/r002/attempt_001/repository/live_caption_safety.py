import json

from speech_client import bedrock_runtime_client
from speech_models import normalize_text


def live_caption_safety(payload, config=None):
    client = bedrock_runtime_client(config)
    model_id = (config or {}).get("model_id") or "anthropic.claude-3-haiku-20240307-v1:0"
    prompt = f"Classify whether this caption contains unsafe content. Return only JSON with unsafe boolean and reason. Caption: {normalize_text(payload['text'])}"
    body = json.dumps({"anthropic_version": "bedrock-2023-05-31", "max_tokens": 128, "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]})
    response = client.invoke_model(modelId=model_id, body=body)
    data = json.loads(response["body"].read())
    return {"text": payload["text"], "unsafe": "unsafe" in data["content"][0]["text"].lower()}
