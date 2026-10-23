from typing import List, Tuple
from embed_text import embed_text
from embed_batch import embed_batch
from embeddings_models import CombinedEmbeddingResult

def embed_for_search(query: str, documents: List[str]) -> Tuple[CombinedEmbeddingResult, List[CombinedEmbeddingResult]]:
    query_embedding_result = embed_text(query)
    document_embedding_results = embed_batch(documents)
    return query_embedding_result, document_embedding_results
