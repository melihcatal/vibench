import json

from embeddings_client import bedrock_client, model_id
from embeddings_models import normalize_embedding_response


def embed_batch(payload, config=None):
    client = bedrock_client(config)
    response = client.invoke_model(modelId=model_id(config), body=json.dumps({"inputTextList": payload["texts"]}), contentType="application/json", accept="application/json")
    stream = response["body"]
    try:
        return normalize_embedding_response(json.loads(stream.read()))
    finally:
        stream.close()
