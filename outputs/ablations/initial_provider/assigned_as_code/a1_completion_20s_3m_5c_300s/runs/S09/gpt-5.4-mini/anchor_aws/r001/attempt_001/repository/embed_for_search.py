from embeddings_client import get_bedrock_client, get_model_id, invoke_embedding
from embeddings_models import normalize_query_and_documents, parse_embedding_response


def embed_for_search(payload, config=None):
    query, documents = normalize_query_and_documents(payload)
    client = get_bedrock_client(config)
    model_id = get_model_id(config)
    query_embedding = parse_embedding_response(invoke_embedding(client, model_id, query))["embedding"]
    document_embeddings = []
    for document in documents:
        document_embeddings.append(parse_embedding_response(invoke_embedding(client, model_id, document))["embedding"])
    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
