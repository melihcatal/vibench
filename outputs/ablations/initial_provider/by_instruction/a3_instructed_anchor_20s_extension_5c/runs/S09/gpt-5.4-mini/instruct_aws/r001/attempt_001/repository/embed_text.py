import json

from embeddings_client import create_bedrock_runtime_client
from embeddings_models import normalize_texts, parse_bedrock_embedding_response


def embed_text(text):
    client, cfg = create_bedrock_runtime_client()
    payload = json.dumps({"inputText": normalize_texts(text)[0]})
    response = client.invoke_model(modelId=cfg.model_id, body=payload)
    return parse_bedrock_embedding_response(response["body"].read())
