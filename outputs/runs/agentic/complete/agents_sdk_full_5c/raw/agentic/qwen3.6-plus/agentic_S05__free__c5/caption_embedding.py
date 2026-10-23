"""Embed caption chunks for semantic meeting search using Google Cloud Vertex AI.

Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
SDK: vertexai (google.cloud.aiplatform)
Model: textembedding-gecko (Google's text embedding model)
"""

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import vertexai
from vertexai.language_models import TextEmbeddingModel


VERTEX_AI_HOST = "aiplatform.googleapis.com"
VERTEX_AI_EMBEDDING_MODEL = "textembedding-gecko@003"
VERTEX_AI_LOCATION = "us-central1"


@dataclass
class CaptionEmbedding:
    """Embedding result for a caption chunk.

    Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
    Model: textembedding-gecko@003
    """
    caption_text: str = ""
    embedding: list[float] = field(default_factory=list)
    dimensions: int = 0
    is_final: bool = False
    timestamp: float = 0.0

    @property
    def numpy_embedding(self) -> np.ndarray:
        """Return embedding as a numpy array for similarity computation."""
        return np.array(self.embedding, dtype=np.float32)


def initialize_vertex_ai(
    project_id: Optional[str] = None,
    location: str = VERTEX_AI_LOCATION,
) -> None:
    """Initialize Vertex AI SDK for embedding operations.

    Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
    SDK: vertexai (google.cloud.aiplatform)
    """
    vertexai.init(project=project_id, location=location)


def get_embedding_model(
    model_name: str = VERTEX_AI_EMBEDDING_MODEL,
) -> TextEmbeddingModel:
    """Get a Vertex AI text embedding model.

    Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
    Model: textembedding-gecko@003 (768-dimensional embeddings)

    Available models:
        - textembedding-gecko@003: Latest Gecko model, 768 dimensions
        - textembedding-gecko@002: Previous version, 768 dimensions
        - textembedding-gecko: Base version
    """
    return TextEmbeddingModel.from_pretrained(model_name)


def embed_caption(
    caption_text: str,
    project_id: Optional[str] = None,
    model_name: str = VERTEX_AI_EMBEDDING_MODEL,
    is_final: bool = False,
    timestamp: float = 0.0,
) -> CaptionEmbedding:
    """Generate embedding for a caption chunk using Google Cloud Vertex AI.

    Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
    Model: textembedding-gecko@003

    Args:
        caption_text: Caption text to embed
        project_id: Google Cloud project ID
        model_name: Vertex AI embedding model identifier
        is_final: Whether this is a final (non-interim) caption
        timestamp: Timestamp of the caption

    Returns:
        CaptionEmbedding with vector representation
    """
    if not caption_text or not caption_text.strip():
        return CaptionEmbedding(
            caption_text=caption_text,
            is_final=is_final,
            timestamp=timestamp,
        )

    initialize_vertex_ai(project_id=project_id)
    model = get_embedding_model(model_name)

    embeddings = model.get_embeddings([caption_text])

    if embeddings:
        embedding_vector = embeddings[0].values
        return CaptionEmbedding(
            caption_text=caption_text,
            embedding=embedding_vector,
            dimensions=len(embedding_vector),
            is_final=is_final,
            timestamp=timestamp,
        )

    return CaptionEmbedding(
        caption_text=caption_text,
        is_final=is_final,
        timestamp=timestamp,
    )


def compute_similarity(
    embedding_a: CaptionEmbedding,
    embedding_b: CaptionEmbedding,
    metric: str = "cosine",
) -> float:
    """Compute similarity between two caption embeddings.

    Uses numpy for cosine similarity computation.

    Args:
        embedding_a: First caption embedding
        embedding_b: Second caption embedding
        metric: Similarity metric ('cosine')

    Returns:
        Similarity score between 0 and 1
    """
    vec_a = embedding_a.numpy_embedding
    vec_b = embedding_b.numpy_embedding

    if len(vec_a) == 0 or len(vec_b) == 0:
        return 0.0

    if metric == "cosine":
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

    return 0.0


class CaptionEmbedder:
    """Stateless embedder for live caption chunks.

    Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
    Model: textembedding-gecko@003
    """

    def __init__(
        self,
        project_id: Optional[str] = None,
        model_name: str = VERTEX_AI_EMBEDDING_MODEL,
    ):
        self.project_id = project_id
        self.model_name = model_name
        self._embeddings: list[CaptionEmbedding] = []

    def embed(self, caption_text: str, is_final: bool = False, timestamp: float = 0.0) -> CaptionEmbedding:
        """Embed a caption chunk.

        Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
        Model: textembedding-gecko@003
        """
        result = embed_caption(
            caption_text=caption_text,
            project_id=self.project_id,
            model_name=self.model_name,
            is_final=is_final,
            timestamp=timestamp,
        )
        self._embeddings.append(result)
        return result

    def search_similar(
        self, query_text: str, top_k: int = 5
    ) -> list[tuple[CaptionEmbedding, float]]:
        """Find most similar captions to a query text.

        Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
        Model: textembedding-gecko@003
        """
        query_embedding = embed_caption(
            query_text,
            project_id=self.project_id,
            model_name=self.model_name,
        )

        if not query_embedding.embedding:
            return []

        scored = []
        for cap_embed in self._embeddings:
            if cap_embed.embedding:
                sim = compute_similarity(query_embedding, cap_embed)
                scored.append((cap_embed, sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    @property
    def all_embeddings(self) -> list[CaptionEmbedding]:
        """Return all stored embeddings."""
        return list(self._embeddings)
