from embeddings_client import embed_texts
from embeddings_models import vector_from_response


def embed_batch(texts, model=None):
    response = embed_texts(texts, model=model)
    if hasattr(response, "embeddings"):
        return [list(item.values) for item in response.embeddings]
    if isinstance(response, dict) and "embeddings" in response:
        return [list(item.get("values", [])) for item in response["embeddings"]]
    return [vector_from_response(response)]
