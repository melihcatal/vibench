import os
from typing import List, Optional, Iterator
import numpy as np
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel


class CaptionEmbedder:
    def __init__(
        self,
        model_name: str = "textembedding-gecko@003",
        dimensionality: Optional[int] = None,
    ):
        self.model_name = model_name
        self.dimensionality = dimensionality
        self._embeddings: List[List[float]] = []
        self._texts: List[str] = []
        self._initialized = False

    def initialize(self, project: Optional[str] = None, location: str = "us-central1"):
        if not self._initialized:
            aiplatform.init(
                project=project or os.environ.get("GOOGLE_CLOUD_PROJECT"),
                location=location,
            )
            self._initialized = True

    def _get_model(self) -> TextEmbeddingModel:
        self.initialize()
        return TextEmbeddingModel.from_pretrained(self.model_name)

    def embed_text(self, text: str) -> List[float]:
        model = self._get_model()
        kwargs = {}
        if self.dimensionality:
            kwargs["dimensionality"] = self.dimensionality

        embeddings = model.get_embeddings([text], **kwargs)
        return embeddings[0].values

    def embed_batch(self, texts: List[str], batch_size: int = 5) -> List[List[float]]:
        model = self._get_model()
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            kwargs = {}
            if self.dimensionality:
                kwargs["dimensionality"] = self.dimensionality

            embeddings = model.get_embeddings(batch, **kwargs)
            for emb in embeddings:
                all_embeddings.append(emb.values)

        return all_embeddings

    def add_caption(self, caption: str):
        if caption.strip():
            self._texts.append(caption)
            embedding = self.embed_text(caption)
            self._embeddings.append(embedding)

    def add_captions_batch(self, captions: List[str]):
        if captions:
            self._texts.extend(captions)
            embeddings = self.embed_batch(captions)
            self._embeddings.extend(embeddings)

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        if not self._embeddings:
            return []

        query_embedding = self.embed_text(query)
        query_vec = np.array(query_embedding)
        embedding_matrix = np.array(self._embeddings)

        query_norm = np.linalg.norm(query_vec)
        matrix_norms = np.linalg.norm(embedding_matrix, axis=1)

        similarities = np.dot(embedding_matrix, query_vec) / (
            matrix_norms * query_norm + 1e-8
        )

        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append(
                {
                    "text": self._texts[idx],
                    "similarity": float(similarities[idx]),
                    "index": int(idx),
                }
            )

        return results

    def get_embeddings(self) -> List[List[float]]:
        return list(self._embeddings)

    def get_texts(self) -> List[str]:
        return list(self._texts)

    def clear(self):
        self._embeddings.clear()
        self._texts.clear()


def embed_caption(
    text: str,
    model_name: str = "textembedding-gecko@003",
) -> List[float]:
    embedder = CaptionEmbedder(model_name=model_name)
    return embedder.embed_text(text)


def embed_caption_stream(
    caption_stream: Iterator[str],
    model_name: str = "textembedding-gecko@003",
) -> Iterator[dict]:
    embedder = CaptionEmbedder(model_name=model_name)
    for caption in caption_stream:
        if caption.strip():
            embedding = embedder.embed_text(caption)
            yield {
                "text": caption,
                "embedding": embedding,
                "dimensionality": len(embedding),
            }


def create_semantic_search_index(
    captions: List[str],
    model_name: str = "textembedding-gecko@003",
) -> CaptionEmbedder:
    embedder = CaptionEmbedder(model_name=model_name)
    embedder.add_captions_batch(captions)
    return embedder
