import os
import uuid
from typing import List, Optional
import openai
from translation_models import EmbeddingSegment, TranslationMemoryIndex

OPENAI_EMBEDDINGS_ENDPOINT = "https://api.openai.com/v1/embeddings"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536


def get_openai_client() -> openai.OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return openai.OpenAI(api_key=api_key)


def create_embedding(
    client: openai.OpenAI, text: str, model: str = EMBEDDING_MODEL
) -> List[float]:
    response = client.embeddings.create(
        model=model,
        input=text,
        dimensions=EMBEDDING_DIMENSION,
    )
    return response.data[0].embedding


def embed_translated_segments(
    texts: List[str],
    source_lang: str = "EN",
    target_lang: str = "ES",
    index_name: Optional[str] = None,
) -> TranslationMemoryIndex:
    client = get_openai_client()
    segments = []
    for text in texts:
        if not text or not text.strip():
            continue
        embedding = create_embedding(client, text)
        segment_id = str(uuid.uuid4())[:8]
        segments.append(
            EmbeddingSegment(
                text=text,
                embedding=embedding,
                source_lang=source_lang,
                target_lang=target_lang,
                segment_id=segment_id,
            )
        )
    return TranslationMemoryIndex(
        segments=segments,
        index_name=index_name or f"tm_{source_lang.lower()}_{target_lang.lower()}",
        embedding_model=EMBEDDING_MODEL,
        dimension=EMBEDDING_DIMENSION,
    )


def search_translation_memory(
    query: str,
    index: TranslationMemoryIndex,
    top_k: int = 5,
) -> List[EmbeddingSegment]:
    client = get_openai_client()
    query_embedding = create_embedding(client, query)
    scored_segments = []
    for segment in index.segments:
        similarity = cosine_similarity(query_embedding, segment.embedding)
        scored_segments.append((similarity, segment))
    scored_segments.sort(key=lambda x: x[0], reverse=True)
    return [segment for _, segment in scored_segments[:top_k]]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)
