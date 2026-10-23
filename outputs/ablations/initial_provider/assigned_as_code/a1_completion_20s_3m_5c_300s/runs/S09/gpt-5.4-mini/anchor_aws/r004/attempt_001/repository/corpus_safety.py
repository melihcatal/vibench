import re

from embeddings_client import get_bedrock_client, get_model_id, invoke_bedrock_json


def corpus_safety(payload, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    model_id = get_model_id(config)
    text = payload["text"]
    invoke_bedrock_json(client, model_id, {"inputText": text})
    return {"safe": not bool(re.search(r"\b(password|secret|token)\b", text, re.I))}
