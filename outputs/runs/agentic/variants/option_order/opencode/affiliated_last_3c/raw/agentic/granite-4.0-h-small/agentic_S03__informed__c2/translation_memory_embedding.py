import sentence_transformers
from typing import List


class TranslationMemoryEmbedder:
    """Embed translated segments for building or querying translation memory."""

    def __init__(self, model_id: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = sentence_transformers.SentenceTransformer(model_id)

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Return embeddings for a list of translated sentences."""
        return self.model.encode(texts, convert_to_tensor=True).tolist()

    def find_similar(
        self,
        query_embedding: List[float],
        memory_embeddings: List[List[float]],
        top_k: int = 5,
    ) -> List[tuple]:
        """Simple nearest-neighbor search (placeholder). Real implementation should use efficient vector DB."""
        import scipy.spatial.distance

        distances = [
            scipy.spatial.distance.cosine(query_embedding, mem)
            for mem in memory_embeddings
        ]
        nearest_indices = sorted(range(len(distances)), key=lambda i: distances[i])[
            :top_k
        ]
        return [(i, distances[i]) for i in nearest_indices]
