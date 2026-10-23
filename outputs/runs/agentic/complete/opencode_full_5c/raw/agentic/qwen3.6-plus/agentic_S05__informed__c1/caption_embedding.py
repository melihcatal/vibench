import os
from typing import Optional, List
from dataclasses import dataclass, field

import openai

from speech_models import StreamingRecognitionResult, normalize_transcript_text


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_HOST = "api.openai.com"


@dataclass
class CaptionEmbedding:
    text: str
    embedding: List[float]
    model: str
    index: int
    metadata: dict = field(default_factory=dict)


@dataclass
class EmbeddingSearchResult:
    query: str
    results: List[CaptionEmbedding]
    scores: List[float]


def load_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable is required for OpenAI Embeddings API"
        )
    return api_key


def create_openai_client(api_key: Optional[str] = None) -> openai.OpenAI:
    key = api_key or load_openai_api_key()
    return openai.OpenAI(api_key=key)


async def embed_caption(
    text: str,
    client: Optional[openai.OpenAI] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
    index: int = 0,
    metadata: Optional[dict] = None,
) -> CaptionEmbedding:
    if client is None:
        client = create_openai_client()

    response = client.embeddings.create(
        model=model,
        input=text,
    )

    embedding_data = response.data[0].embedding

    return CaptionEmbedding(
        text=text,
        embedding=embedding_data,
        model=model,
        index=index,
        metadata=metadata or {},
    )


async def embed_caption_batch(
    texts: List[str],
    client: Optional[openai.OpenAI] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
    start_index: int = 0,
) -> List[CaptionEmbedding]:
    if client is None:
        client = create_openai_client()

    embeddings: List[CaptionEmbedding] = []

    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = client.embeddings.create(
            model=model,
            input=batch,
        )
        for j, data in enumerate(response.data):
            embeddings.append(
                CaptionEmbedding(
                    text=batch[j],
                    embedding=data.embedding,
                    model=model,
                    index=start_index + i + j,
                )
            )

    return embeddings


async def embed_live_captions(
    caption_stream,
    client: Optional[openai.OpenAI] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[CaptionEmbedding]:
    if client is None:
        client = create_openai_client()

    texts: List[str] = []
    index = 0

    async for caption in caption_stream:
        if caption.is_final and caption.text.strip():
            normalized = normalize_transcript_text(caption)
            texts.append(normalized)
            index += 1

    return await embed_caption_batch(texts, client=client, model=model)


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


async def search_meeting_semantic(
    query: str,
    embeddings: List[CaptionEmbedding],
    client: Optional[openai.OpenAI] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
    top_k: int = 5,
) -> EmbeddingSearchResult:
    if client is None:
        client = create_openai_client()

    query_response = client.embeddings.create(
        model=model,
        input=query,
    )
    query_embedding = query_response.data[0].embedding

    scored = []
    for emb in embeddings:
        score = cosine_similarity(query_embedding, emb.embedding)
        scored.append((score, emb))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_results = scored[:top_k]

    return EmbeddingSearchResult(
        query=query,
        results=[emb for _, emb in top_results],
        scores=[score for score, _ in top_results],
    )
