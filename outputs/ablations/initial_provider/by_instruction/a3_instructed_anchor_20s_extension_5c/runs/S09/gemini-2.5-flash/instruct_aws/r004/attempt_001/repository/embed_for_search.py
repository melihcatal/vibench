from embed_text import embed_text
from embed_batch import embed_batch

def embed_for_search(
    query_text: str,
    document_texts: list[str]
) -> tuple[list[float], list[list[float]]]:
    """
    Embeds a query and a list of documents for semantic search using AWS Bedrock.
    Returns the query embedding and a list of document embeddings.
    """
    query_embedding = embed_text(query_text)
    document_embeddings = embed_batch(document_texts)

    return query_embedding, document_embeddings
