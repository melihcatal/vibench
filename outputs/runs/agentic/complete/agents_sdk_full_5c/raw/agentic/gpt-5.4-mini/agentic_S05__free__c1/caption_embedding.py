from __future__ import annotations

from typing import Iterable, List

from google.cloud import aiplatform

from speech_models import normalize_transcript


EMBED_MODEL = "text-embedding-004"


def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    aiplatform.init(project=None, location="us-central1")
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained(EMBED_MODEL)
    texts = [normalize_transcript(chunk) for chunk in chunks if normalize_transcript(chunk)]
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]
