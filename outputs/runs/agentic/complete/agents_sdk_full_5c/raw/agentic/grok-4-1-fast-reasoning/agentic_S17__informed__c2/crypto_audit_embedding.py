import os
import cohere
from typing import List
from security_models import EmbeddingResponse

def crypto_audit_embedding(audit_notes: List[str]) -> List[EmbeddingResponse]:
    """
    Embeds crypto audit notes for semantic search using Cohere Embed API.
    """
    api_key = os.getenv('COHERE_API_KEY')
    co = cohere.Client(api_key)
    response = co.embed(
        texts=audit_notes,
        model='embed-english-v3.0',
        input_type='search_query'
    )
    return [{"embedding": emb, "model": "embed-english-v3.0"} for emb in response.embeddings]