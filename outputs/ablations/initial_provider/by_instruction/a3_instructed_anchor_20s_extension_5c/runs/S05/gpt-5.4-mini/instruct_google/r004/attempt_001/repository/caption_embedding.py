from typing import Iterable, List

from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

from speech_models import normalize_transcript


def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    texts = [normalize_transcript(chunk) for chunk in chunks if chunk]
    return [embedding.values for embedding in model.get_embeddings(texts)]
