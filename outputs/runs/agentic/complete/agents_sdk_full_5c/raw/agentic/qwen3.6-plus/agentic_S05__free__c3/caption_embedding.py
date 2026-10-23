"""
Embed caption chunks for semantic meeting search using Google Cloud Vertex AI.

Uses the google-cloud-aiplatform SDK to generate text embeddings via the
text-embedding-004 model (textembedding-gecko) on Vertex AI at
aiplatform.googleapis.com for semantic search over meeting captions.
"""

from typing import Optional

import vertexai
from vertexai.language_models import TextEmbeddingModel, TextEmbeddingInput

# Google Cloud Vertex AI embedding provider signals
VERTEX_AI_ENDPOINT = "aiplatform.googleapis.com"
VERTEX_AI_EMBEDDING_MODEL_ID = "text-embedding-004"
VERTEX_AI_EMBEDDING_MODEL_FAMILY = "text-embedding-gecko"
VERTEX_AI_LOCATION = "us-central1"


class CaptionEmbedder:
    """
    Generates text embeddings for caption chunks using Vertex AI text-embedding-004.

    Wraps vertexai.language_models.TextEmbeddingModel to create vector embeddings
    of meeting caption text, enabling semantic search over meeting transcripts
    via aiplatform.googleapis.com.
    """

    def __init__(
        self,
        project_id: str,
        location: str = VERTEX_AI_LOCATION,
        model_id: str = VERTEX_AI_EMBEDDING_MODEL_ID,
    ):
        self.project_id = project_id
        self.location = location
        self.model_id = model_id

        vertexai.init(
            project=self.project_id,
            location=self.location,
        )

        self.model = TextEmbeddingModel.from_pretrained(self.model_id)
        self._embeddings_store: dict[str, list[float]] = {}
        self._embedding_count = 0

    def embed_caption(self, caption_text: str, caption_id: Optional[str] = None) -> list[float]:
        """
        Generate an embedding vector for a single caption chunk.

        Uses Vertex AI's text-embedding-004 model (text-embedding-gecko family)
        via aiplatform.googleapis.com to produce a vector representation of the text.

        Args:
            caption_text: Caption text to embed.
            caption_id: Optional identifier for the caption chunk.

        Returns:
            List of floats representing the embedding vector (768 dimensions).
        """
        if not caption_text or not caption_text.strip():
            return []

        task = TextEmbeddingInput(
            text=caption_text,
            task_type="RETRIEVAL_DOCUMENT",
        )

        embeddings = self.model.get_embeddings([task])

        if embeddings and embeddings[0].values:
            vector = embeddings[0].values

            if caption_id:
                self._embeddings_store[caption_id] = vector
                self._embedding_count += 1

            return vector

        return []

    def embed_captions_batch(
        self,
        caption_texts: list[str],
        caption_ids: Optional[list[str]] = None,
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple caption chunks in a batch.

        Sends a batch of texts to Vertex AI text-embedding-004 model for
        efficient vector generation via aiplatform.googleapis.com.

        Args:
            caption_texts: List of caption text strings to embed.
            caption_ids: Optional list of identifiers corresponding to each caption.

        Returns:
            List of embedding vectors, one per input caption.
        """
        if not caption_texts:
            return []

        tasks = [
            TextEmbeddingInput(text=t, task_type="RETRIEVAL_DOCUMENT")
            for t in caption_texts
            if t and t.strip()
        ]

        if not tasks:
            return []

        embeddings = self.model.get_embeddings(tasks)

        vectors = []
        for i, emb in enumerate(embeddings):
            if emb.values:
                vector = emb.values
                vectors.append(vector)

                if caption_ids and i < len(caption_ids) and caption_ids[i]:
                    self._embeddings_store[caption_ids[i]] = vector
                    self._embedding_count += 1
            else:
                vectors.append([])

        return vectors

    def store_embedding(self, caption_id: str, embedding: list[float]):
        """Manually store an embedding with a caption ID."""
        self._embeddings_store[caption_id] = embedding
        self._embedding_count += 1

    def get_stored_embedding(self, caption_id: str) -> Optional[list[float]]:
        """Retrieve a previously stored embedding by caption ID."""
        return self._embeddings_store.get(caption_id)

    @property
    def embedding_count(self) -> int:
        return self._embedding_count

    @staticmethod
    def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
        """
        Compute cosine similarity between two embedding vectors.

        Used for semantic search over stored caption embeddings.

        Args:
            vec_a: First embedding vector.
            vec_b: Second embedding vector.

        Returns:
            Cosine similarity score between -1.0 and 1.0.
        """
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        magnitude_a = sum(a * a for a in vec_a) ** 0.5
        magnitude_b = sum(b * b for b in vec_b) ** 0.5

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)


def create_caption_embedder(
    project_id: str,
    location: str = VERTEX_AI_LOCATION,
    model_id: str = VERTEX_AI_EMBEDDING_MODEL_ID,
) -> CaptionEmbedder:
    """
    Factory function to create a CaptionEmbedder using Vertex AI embeddings.

    Args:
        project_id: Google Cloud project ID.
        location: Vertex AI region.
        model_id: Text embedding model identifier (text-embedding-004).

    Returns:
        Configured CaptionEmbedder instance.
    """
    return CaptionEmbedder(
        project_id=project_id,
        location=location,
        model_id=model_id,
    )
