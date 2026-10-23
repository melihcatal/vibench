import os
import hashlib
from typing import Dict, List, Optional, Tuple

import dashscope
from dashscope import TextEmbedding

from speech_models import TranscriptResult

EMBEDDING_MODEL = "text-embedding-v3"


def get_dashscope_api_key() -> str:
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable is not set")
    return api_key


def configure_dashscope(api_key: Optional[str] = None):
    key = api_key or get_dashscope_api_key()
    dashscope.api_key = key


def embed_text(
    text: str,
    model: str = EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> List[float]:
    configure_dashscope(api_key)

    response = TextEmbedding.call(
        model=model,
        input=text,
    )

    if response.status_code == 200:
        embedding = response.output["embeddings"][0]["embedding"]
        return embedding
    else:
        raise RuntimeError(
            f"DashScope Embeddings API error: {response.code} - {response.message}"
        )


def embed_texts_batch(
    texts: List[str],
    model: str = EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    batch_size: int = 25,
) -> List[List[float]]:
    configure_dashscope(api_key)

    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = TextEmbedding.call(
            model=model,
            input=batch,
        )

        if response.status_code == 200:
            batch_embeddings = [
                item["embedding"] for item in response.output["embeddings"]
            ]
            all_embeddings.extend(batch_embeddings)
        else:
            raise RuntimeError(
                f"DashScope Embeddings API error: {response.code} - {response.message}"
            )

    return all_embeddings


def embed_transcript_result(
    result: TranscriptResult,
    model: str = EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> Dict:
    embedding = embed_text(result.text, model=model, api_key=api_key)
    return {
        "result_id": result.result_id,
        "text": result.text,
        "embedding": embedding,
        "timestamp": result.timestamp,
        "is_final": result.is_final,
        "language": result.language,
    }


def compute_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    if len(embedding1) != len(embedding2):
        raise ValueError("Embeddings must have the same dimension")

    dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
    norm1 = sum(a * a for a in embedding1) ** 0.5
    norm2 = sum(b * b for b in embedding2) ** 0.5

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


class CaptionEmbeddingIndex:
    def __init__(
        self,
        model: str = EMBEDDING_MODEL,
        api_key: Optional[str] = None,
    ):
        self.model = model
        self.api_key = api_key
        self._index: Dict[str, Dict] = {}
        self._text_to_id: Dict[str, str] = {}

    def add_result(self, result: TranscriptResult) -> Dict:
        if result.text in self._text_to_id:
            return self._index[self._text_to_id[result.text]]

        embedded = embed_transcript_result(
            result, model=self.model, api_key=self.api_key
        )
        self._index[embedded["result_id"]] = embedded
        self._text_to_id[result.text] = embedded["result_id"]
        return embedded

    def add_text(self, text: str, metadata: Optional[Dict] = None) -> Dict:
        text_id = hashlib.md5(text.encode()).hexdigest()
        if text_id in self._index:
            return self._index[text_id]

        embedding = embed_text(text, model=self.model, api_key=self.api_key)
        record = {
            "result_id": text_id,
            "text": text,
            "embedding": embedding,
            "timestamp": metadata.get("timestamp", 0) if metadata else 0,
            "is_final": metadata.get("is_final", True) if metadata else True,
            "language": metadata.get("language", "en") if metadata else "en",
        }
        self._index[text_id] = record
        self._text_to_id[text] = text_id
        return record

    def search(
        self,
        query_text: str,
        top_k: int = 5,
        min_similarity: float = 0.0,
    ) -> List[Tuple[Dict, float]]:
        query_embedding = embed_text(query_text, model=self.model, api_key=self.api_key)

        scored_results = []
        for record_id, record in self._index.items():
            similarity = compute_similarity(query_embedding, record["embedding"])
            if similarity >= min_similarity:
                scored_results.append((record, similarity))

        scored_results.sort(key=lambda x: x[1], reverse=True)
        return scored_results[:top_k]

    def search_by_embedding(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        min_similarity: float = 0.0,
    ) -> List[Tuple[Dict, float]]:
        scored_results = []
        for record_id, record in self._index.items():
            similarity = compute_similarity(query_embedding, record["embedding"])
            if similarity >= min_similarity:
                scored_results.append((record, similarity))

        scored_results.sort(key=lambda x: x[1], reverse=True)
        return scored_results[:top_k]

    def get_all_embeddings(self) -> List[Dict]:
        return list(self._index.values())

    def size(self) -> int:
        return len(self._index)

    def clear(self):
        self._index.clear()
        self._text_to_id.clear()
