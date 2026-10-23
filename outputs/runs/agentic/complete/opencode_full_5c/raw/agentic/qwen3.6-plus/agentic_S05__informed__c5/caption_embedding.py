import os
from typing import Optional, List

from openai import OpenAI

from speech_models import FinalTranscript


def load_openai_config() -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return {"api_key": api_key}


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    if api_key is None:
        config = load_openai_config()
        api_key = config["api_key"]
    return OpenAI(api_key=api_key)


async def embed_caption_chunk(
    transcript: FinalTranscript,
    client: Optional[OpenAI] = None,
    model: str = "text-embedding-3-small",
) -> List[float]:
    if client is None:
        client = create_openai_client()

    text = transcript.text
    if not text:
        return []

    response = client.embeddings.create(
        model=model,
        input=text,
    )

    embedding = response.data[0].embedding
    return embedding


async def embed_caption_stream(
    transcript_stream,
    client: Optional[OpenAI] = None,
    model: str = "text-embedding-3-small",
):
    if client is None:
        client = create_openai_client()

    async for item in transcript_stream:
        if isinstance(item, FinalTranscript):
            embedding = await embed_caption_chunk(item, client=client, model=model)
            yield {
                "text": item.text,
                "embedding": embedding,
                "timestamp": item.timestamp,
            }
        elif hasattr(item, "final") and item.final:
            embedding = await embed_caption_chunk(
                item.final, client=client, model=model
            )
            yield {
                "text": item.final.text,
                "embedding": embedding,
                "timestamp": item.final.timestamp,
            }


def compute_similarity(embedding_a: List[float], embedding_b: List[float]) -> float:
    if not embedding_a or not embedding_b:
        return 0.0

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)
