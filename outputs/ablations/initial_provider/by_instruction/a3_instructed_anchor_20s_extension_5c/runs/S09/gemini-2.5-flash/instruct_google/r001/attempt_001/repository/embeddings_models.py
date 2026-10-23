from typing import List, Dict, Any, Union
from dataclasses import dataclass

@dataclass
class EmbeddingRequest:
    text: Union[str, List[str]]

@dataclass
class EmbeddingResponse:
    embedding: Union[List[float], List[List[float]]]

def normalize_embedding_response(raw_response: Dict[str, Any]) -> Union[List[float], List[List[float]]]:
    """Normalizes the raw response from the Google Generative AI embeddings API.

    Args:
        raw_response: The raw dictionary response from the API.

    Returns:
        A list of floats for single embedding or a list of list of floats for batch embeddings.
    """
    if "embedding" in raw_response:
        return raw_response["embedding"]
    elif "embeddings" in raw_response:
        return [item["embedding"] for item in raw_response["embeddings"]]
    else:
        raise ValueError("Unexpected embedding response format.")

