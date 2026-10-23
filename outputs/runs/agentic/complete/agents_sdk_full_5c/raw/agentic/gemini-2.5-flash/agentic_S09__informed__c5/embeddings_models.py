from typing import List, Dict, Any

class EmbeddingResult:
    """Represents a simplified embedding result structure."""
    def __init__(self, embedding: List[float]):
        self.embedding = embedding

    @classmethod
    def from_gemini_response(cls, response: Dict[str, Any]) -> List['EmbeddingResult']:
        """Normalizes a Gemini API embedding response into a list of EmbeddingResult objects."""
        results = []
        if "embedding" in response:
            results.append(cls(embedding=response["embedding"]))
        elif "embeddings" in response:
            for item in response["embeddings"]:
                results.append(cls(embedding=item["embedding"]))
        return results

