from typing import List, Dict, Any, Optional
import numpy as np


class EmbeddingRequest:
    """Normalized request for embeddings."""

    def __init__(self, texts: List[str], model_id: str = "ibm/slate-125m-english-rtrvr"):
        self.texts = texts
        self.model_id = model_id

    def to_provider_payload(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "inputs": self.texts,
            "parameters": {"truncate_input_tokens": 512}
        }


class EmbeddingResponse:
    """Normalized response for embeddings."""

    def __init__(self, provider_response: Dict[str, Any]):
        self.provider_response = provider_response
        self.embeddings = self._extract_embeddings()

    def _extract_embeddings(self) -> List[List[float]]:
        return [item["embedding"] for item in self.provider_response.get("results", [])]

    def to_numpy(self) -> np.ndarray:
        return np.array(self.embeddings)


class SimilarityScorer:
    """Helper for computing cosine similarity."""

    @staticmethod
    def cosine_similarity(a: List[float], b: List[float]) -> float:
        a_arr = np.array(a)
        b_arr = np.array(b)
        dot_product = np.dot(a_arr, b_arr)
        norm_a = np.linalg.norm(a_arr)
        norm_b = np.linalg.norm(b_arr)
        return float(dot_product / (norm_a * norm_b))