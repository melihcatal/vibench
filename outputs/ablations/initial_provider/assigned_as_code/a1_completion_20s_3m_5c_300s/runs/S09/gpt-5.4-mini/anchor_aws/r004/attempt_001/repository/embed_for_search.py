from embeddings_client import get_bedrock_client, get_model_id, invoke_bedrock_json
from embeddings_models import parse_embedding_response


def embed_for_search(payload, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    model_id = get_model_id(config)
    query = invoke_bedrock_json(client, model_id, {"inputText": payload["query"]})
    documents = []
    for document in payload.get("documents", []):
        documents.append(parse_embedding_response(invoke_bedrock_json(client, model_id, {"inputText": document})))
    return {"query_embedding": parse_embedding_response(query), "document_embeddings": documents}
