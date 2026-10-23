import json

from embeddings_client import create_bedrock_runtime_client
from embeddings_models import normalize_texts, parse_bedrock_embedding_response


def embed_batch(texts):
    client, cfg = create_bedrock_runtime_client()
    outputs = []
    for text in normalize_texts(texts):
        response = client.invoke_model(modelId=cfg.model_id, body=json.dumps({"inputText": text}))
        outputs.append(parse_bedrock_embedding_response(response["body"].read()))
    return outputs
