import os
from openai import OpenAI

from model_models import EmbeddingRequest, EmbeddingResponse

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_EMBED_MODEL = "text-embedding-3-small"


def get_openai_client() -> OpenAI:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=OPENAI_API_KEY)


def output_embedding(
    texts: list[str], model: str = OPENAI_EMBED_MODEL
) -> EmbeddingResponse:
    client = get_openai_client()
    response = client.embeddings.create(
        model=model,
        input=texts,
    )

    embeddings = []
    total_tokens = 0
    for item in response.data:
        embeddings.append(item.embedding)
        total_tokens += (
            item.get("usage", {}).get("total_tokens", 0)
            if isinstance(item, dict)
            else 0
        )

    if response.usage:
        total_tokens = response.usage.total_tokens

    return EmbeddingResponse(
        embeddings=embeddings,
        model=response.model,
        total_tokens=total_tokens,
    )
