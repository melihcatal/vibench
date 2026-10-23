from typing import Dict

class EmbeddingsModels:
    """Local helpers for request/response shapes and normalisation."""
    @staticmethod
    def normalize_embedding(vec: List[float]) -> List[float]:
        """Simple L2 normalisation of an embedding vector."""
        import numpy as np
        arr = np.array(vec, dtype=np.float32)
        norm = np.linalg.norm(arr)
        if norm == 0:
            return vec  # avoid division by zero; return zero vector unchanged
        return (arr / norm).tolist()

    @staticmethod
def _build_request(text: str) -> Dict:
        """Internal: shape the payload expected by the provider SDK."""
        return {"texts": [text]}

    @staticmethod
    def _parse_response(resp: dict) -> List[List[float]]:
        """Internal: extract embeddings list from DashScope response format."""
        return resp.get("embeddings", [])
