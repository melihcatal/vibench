import json

from speech_client import bedrock_runtime_client
from speech_models import normalize_text


def meeting_summary(payload, config=None):
    client = bedrock_runtime_client(config)
    model_id = (config or {}).get("model_id") or "anthropic.claude-3-haiku-20240307-v1:0"
    prompt = f"Summarize this meeting transcript chunk concisely: {normalize_text(payload['text'])}"
    body = json.dumps({"anthropic_version": "bedrock-2023-05-31", "max_tokens": 256, "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]})
    response = client.invoke_model(modelId=model_id, body=body)
    data = json.loads(response["body"].read())
    return {"text": data["content"][0]["text"]}
