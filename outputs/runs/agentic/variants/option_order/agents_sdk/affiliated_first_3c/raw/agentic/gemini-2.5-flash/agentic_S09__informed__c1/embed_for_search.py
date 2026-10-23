import embeddings_client
import embeddings_models
from typing import List, Dict, Any

def embed_for_search(
    query_text: str,
    document_texts: List[str]
) -> Dict[str, List[List[float]]]:
    """Embeds a query and a list of documents for semantic search using OpenAI Embeddings.

    Args:
        query_text: The search query string.
        document_texts: A list of document strings to embed.

    Returns:
        A dictionary containing 'query_embedding' and 'document_embeddings'.
    """
    openai = embeddings_client.get_openai_client()
    model_name = embeddings_client.get_embedding_model_name()

    all_texts = [query_text] + document_texts
    prepared_texts = embeddings_models.prepare_batch_for_embedding(all_texts)

    if not prepared_texts:
        return {"query_embedding": [], "document_embeddings": []}

    response = openai.Embedding.create(
        input=prepared_texts,
        model=model_name
    )

    embeddings = embeddings_models.normalize_embedding_response(response)

    query_embedding = embeddings[0] if embeddings else []
    document_embeddings = embeddings[1:] if len(embeddings) > 1 else []

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings
    }
