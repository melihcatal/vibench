from typing import List, Dict, Any, Literal

class EmbeddingRequest:
    text: Union[str, List[str]]
    model: str
    input_type: Optional[Literal["search_document", "search_query", "classification", "clustering"]] = None

class EmbeddingResponse:
    embeddings: List[List[float]]
    model: str
    usage: Dict[str, Any]

class SimilarityScoreResult:
    score: float
    method: str = "cosine_similarity"

class SearchEmbeddings:
    query_embedding: List[List[float]]
    document_embeddings: List[List[float]]