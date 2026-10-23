import json

from speech_client import bedrock_runtime_client
from speech_models import normalize_text


def caption_embedding(payload, config=None):
    client = bedrock_runtime_client(config)
    model_id = (config or {}).get("model_id") or "amazon.titan-embed-text-v2:0"
    body = json.dumps({"inputText": normalize_text(payload['text'])})
    response = client.invoke_model(modelId=model_id, body=body)
    data = json.loads(response["body"].read())
    return {"text": payload["text"], "vector": data.get("embedding") or data.get("embeddings")}
