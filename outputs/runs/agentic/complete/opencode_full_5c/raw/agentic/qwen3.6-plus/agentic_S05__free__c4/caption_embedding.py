from typing import List, Optional, Dict, Any, Tuple
import numpy as np

import vertexai
from vertexai.language_models import TextEmbeddingModel

from speech_models import RecognitionResult


VERTEX_AI_ENDPOINT = "aiplatform.googleapis.com"
EMBEDDING_MODEL = "text-embedding-004"
DEFAULT_LOCATION = "us-central1"
EMBEDDING_DIMENSION = 768


def init_vertex_ai(project_id: str, location: str = DEFAULT_LOCATION):
    vertexai.init(project=project_id, location=location)


def get_embedding_model(
    model_name: str = EMBEDDING_MODEL,
) -> TextEmbeddingModel:
    return TextEmbeddingModel.from_pretrained(model_name)


def embed_text(
    text: str,
    model_name: str = EMBEDDING_MODEL,
    dimensionality: Optional[int] = None,
) -> List[float]:
    model = get_embedding_model(model_name)
    kwargs = {}
    if dimensionality:
        kwargs["dimensionality"] = dimensionality

    embeddings = model.get_embeddings(
        texts=[text],
        **kwargs,
    )
    return embeddings[0].values


def embed_texts(
    texts: List[str],
    model_name: str = EMBEDDING_MODEL,
    dimensionality: Optional[int] = None,
) -> List[List[float]]:
    model = get_embedding_model(model_name)
    kwargs = {}
    if dimensionality:
        kwargs["dimensionality"] = dimensionality

    embeddings = model.get_embeddings(
        texts=texts,
        **kwargs,
    )
    return [e.values for e in embeddings]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    a_np = np.array(a)
    b_np = np.array(b)
    dot_product = np.dot(a_np, b_np)
    norm_a = np.linalg.norm(a_np)
    norm_b = np.linalg.norm(b_np)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))


async def embed_caption_chunk(
    result: RecognitionResult,
    model_name: str = EMBEDDING_MODEL,
) -> Optional[List[float]]:
    transcript = result.best_transcript
    if not transcript:
        return None

    embedding = embed_text(transcript, model_name)
    return embedding


async def embed_captions_stream(
    results,
    model_name: str = EMBEDDING_MODEL,
    on_embedded=None,
):
    async for result in results:
        embedding = await embed_caption_chunk(result, model_name)
        if embedding and on_embedded:
            on_embedded(result, embedding)
        yield embedding


class CaptionEmbeddingStore:
    def __init__(
        self,
        project_id: str,
        model_name: str = EMBEDDING_MODEL,
        location: str = DEFAULT_LOCATION,
    ):
        self.project_id = project_id
        self.model_name = model_name
        self.location = location
        self._embeddings: List[Tuple[str, List[float]]] = []
        self._index: Dict[str, int] = {}

        init_vertex_ai(project_id=project_id, location=location)
        self._model = get_embedding_model(model_name)

    def add_caption(self, result: RecognitionResult) -> Optional[List[float]]:
        transcript = result.best_transcript
        if not transcript:
            return None

        embedding = embed_text(transcript, self.model_name)
        idx = len(self._embeddings)
        self._embeddings.append((transcript, embedding))
        self._index[transcript] = idx
        return embedding

    def search_similar(
        self,
        query_text: str,
        top_k: int = 5,
        threshold: float = 0.7,
    ) -> List[Dict[str, Any]]:
        query_embedding = embed_text(query_text, self.model_name)

        results = []
        for transcript, embedding in self._embeddings:
            similarity = cosine_similarity(query_embedding, embedding)
            if similarity >= threshold:
                results.append(
                    {
                        "transcript": transcript,
                        "similarity": similarity,
                        "embedding": embedding,
                    }
                )

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def get_embedding_count(self) -> int:
        return len(self._embeddings)

    def clear(self):
        self._embeddings.clear()
        self._index.clear()
