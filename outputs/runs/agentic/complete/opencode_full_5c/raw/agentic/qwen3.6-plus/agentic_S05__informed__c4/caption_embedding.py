import os
import asyncio
from typing import Optional, List, Dict, Any

from openai import OpenAI

from speech_models import NormalizedTranscript


def load_openai_config(api_key: Optional[str] = None) -> dict:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return {"api_key": key}


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    config = load_openai_config(api_key)
    return OpenAI(api_key=config["api_key"])


EMBEDDING_MODEL = "text-embedding-3-small"


async def embed_caption_chunk(
    text: str,
    api_key: Optional[str] = None,
    model: str = EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    if client is None:
        client = create_openai_client(api_key)

    loop = asyncio.get_event_loop()

    kwargs = {"input": text, "model": model}
    if dimensions:
        kwargs["dimensions"] = dimensions

    def _create_embedding():
        response = client.embeddings.create(**kwargs)
        return response.data[0].embedding

    embedding = await loop.run_in_executor(None, _create_embedding)

    return {
        "text": text,
        "embedding": embedding,
        "model": model,
        "dimensions": len(embedding),
    }


async def embed_captions_batch(
    captions: List[NormalizedTranscript],
    api_key: Optional[str] = None,
    model: str = EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> List[Dict[str, Any]]:
    if client is None:
        client = create_openai_client(api_key)

    loop = asyncio.get_event_loop()

    texts = [c.text for c in captions if c.text.strip()]
    if not texts:
        return []

    kwargs = {"input": texts, "model": model}
    if dimensions:
        kwargs["dimensions"] = dimensions

    def _create_embeddings():
        response = client.embeddings.create(**kwargs)
        return [data.embedding for data in response.data]

    embeddings = await loop.run_in_executor(None, _create_embeddings)

    results = []
    for i, caption in enumerate(captions):
        if i < len(embeddings):
            results.append(
                {
                    "text": caption.text,
                    "embedding": embeddings[i],
                    "model": model,
                    "dimensions": len(embeddings[i]),
                    "start_time": caption.start_time,
                    "end_time": caption.end_time,
                    "speaker": caption.speaker,
                    "is_final": caption.is_final,
                }
            )

    return results


async def embed_live_caption_stream(
    caption_stream,
    api_key: Optional[str] = None,
    model: str = EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
):
    if client is None:
        client = create_openai_client(api_key)

    async for caption in caption_stream:
        if caption.text.strip():
            result = await embed_caption_chunk(
                text=caption.text,
                api_key=api_key,
                model=model,
                dimensions=dimensions,
                client=client,
            )
            result["start_time"] = caption.start_time
            result["end_time"] = caption.end_time
            result["speaker"] = caption.speaker
            result["is_final"] = caption.is_final
            yield result


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have the same dimension")

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


async def search_similar_meeting_segments(
    query: str,
    indexed_segments: List[Dict[str, Any]],
    api_key: Optional[str] = None,
    model: str = EMBEDDING_MODEL,
    top_k: int = 5,
    threshold: float = 0.7,
) -> List[Dict[str, Any]]:
    query_result = await embed_caption_chunk(
        text=query,
        api_key=api_key,
        model=model,
    )
    query_embedding = query_result["embedding"]

    scored_segments = []
    for segment in indexed_segments:
        if "embedding" in segment:
            similarity = cosine_similarity(query_embedding, segment["embedding"])
            if similarity >= threshold:
                scored_segments.append(
                    {
                        **segment,
                        "similarity_score": similarity,
                    }
                )

    scored_segments.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored_segments[:top_k]
