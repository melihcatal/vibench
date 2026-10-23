
import dataclasses
from typing import Any, Dict, List

@dataclasses.dataclass
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-004" # Default model for demonstration

@dataclasses.dataclass
class EmbeddingResponse:
    embedding: List[float]
    model: str

def _prepare_request(request: EmbeddingRequest) -> Dict[str, Any]:
    """
    Prepares the request payload for the Direct Embeddings API.
    """
    return {
        "model": request.model,
        "content": request.text
    }

def _parse_response(response_data: Dict[str, Any]) -> EmbeddingResponse:
    """
    Parses the response from the Direct Embeddings API.
    """
    # Assuming the API returns a structure like:
    # {"model": "text-embedding-004", "embedding": [0.1, 0.2, ...]}
    embedding_data = response_data.get("embedding", [])
    model_name = response_data.get("model", "")
    return EmbeddingResponse(embedding=embedding_data, model=model_name)

def _normalize_embeddings(embedding: List[float]) -> List[float]:
    """
    Normalizes the embedding vector. (Example: L2 normalization)
    """
    if not embedding:
        return []
    magnitude = sum(x**2 for x in embedding)**0.5
    if magnitude == 0:
        return embedding
    return [x / magnitude for x in embedding]

def create_embedding_request(text: str, model: str = "text-embedding-004") -> Dict[str, Any]:
    """
    Helper to create a full embedding request payload, including preparation.
    """
    request_obj = EmbeddingRequest(text=text, model=model)
    return _prepare_request(request_obj)

def process_embedding_response(response_data: Dict[str, Any]) -> EmbeddingResponse:
    """
    Helper to process an embedding response, including parsing and normalization.
    """
    parsed_response = _parse_response(response_data)
    parsed_response.embedding = _normalize_embeddings(parsed_response.embedding)
    return parsed_response
