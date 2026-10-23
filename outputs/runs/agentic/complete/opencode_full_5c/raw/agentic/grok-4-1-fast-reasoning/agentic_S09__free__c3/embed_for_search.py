from typing import List, Dict
from embeddings_client import embed_texts
from embeddings_models import normalize_texts


def embed_for_search(query: str, documents: List[str]) -> Dict[str, List]:
    """
    Embeds a query and documents for semantic search using OpenAI text-embedding-3-small.
    """
    all_texts = normalize_texts([query] + documents)
    embeddings = embed_texts(all_texts)
    return {"query_embedding": embeddings[0], "document_embeddings": embeddings[1:]}
