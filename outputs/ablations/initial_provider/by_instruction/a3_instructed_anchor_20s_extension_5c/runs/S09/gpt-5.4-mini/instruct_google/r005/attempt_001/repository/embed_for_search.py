from embeddings_client import embed_query, embed_texts
from embeddings_models import vector_from_response


def embed_for_search(query, documents, model=None):
    query_embedding = vector_from_response(embed_query(query, model=model))
    document_embeddings = []
    response = embed_texts(documents, model=model)
    if hasattr(response, "embeddings"):
        document_embeddings = [list(item.values) for item in response.embeddings]
    elif isinstance(response, dict) and "embeddings" in response:
        document_embeddings = [list(item.get("values", [])) for item in response["embeddings"]]
    else:
        document_embeddings = [vector_from_response(response)]
    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
