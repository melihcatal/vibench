from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np


@dataclass
class EmbeddingRequest:
    texts: List[str]
    model: str = "embed-english-v3.0"
    input_type: str = "search_document"


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    meta: Dict[str, Any]


def normalize_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    normalized_embeddings = []
    for emb in embeddings:
        norm = np.linalg.norm(emb)
        if norm > 0:
            normalized_embeddings.append((emb / norm).tolist())
        else:
            normalized_embeddings.append(emb)
    return normalized_embeddings
