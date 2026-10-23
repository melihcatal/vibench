from embeddings_client import get_bedrock_client, get_model_id, invoke_bedrock_json
from embeddings_models import BatchEmbeddingRequest, parse_embedding_response


def embed_batch(payload, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    model_id = get_model_id(config)
    request = BatchEmbeddingRequest(payload["texts"])
    response = invoke_bedrock_json(client, model_id, {"inputTextList": request.to_payload()["texts"]})
    return {"embeddings": [parse_embedding_response(item) for item in response.get("embeddings", [])] or [parse_embedding_response(response)]}
