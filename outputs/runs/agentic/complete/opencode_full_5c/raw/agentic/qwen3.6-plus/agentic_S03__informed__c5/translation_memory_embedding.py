import os
from typing import List, Dict, Any
from openai import OpenAI
from translation_models import (
    TranslationMemoryEmbedRequest,
    TranslationMemoryEmbedResponse,
)

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def _get_openai_client() -> OpenAI:
    api_key = os.environ.get(OPENAI_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"OpenAI API key not found. Set the {OPENAI_API_KEY_ENV} environment variable."
        )
    return OpenAI(api_key=api_key)


def embed_translation_segments(
    request: TranslationMemoryEmbedRequest,
) -> TranslationMemoryEmbedResponse:
    client = _get_openai_client()

    segments = request.segments
    if not segments:
        return TranslationMemoryEmbedResponse(
            embeddings=[],
            segment_count=0,
            model=OPENAI_EMBEDDING_MODEL,
        )

    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=segments,
        encoding_format="float",
    )

    sorted_data = sorted(response.data, key=lambda x: x.index)
    embeddings = [item.embedding for item in sorted_data]

    return TranslationMemoryEmbedResponse(
        embeddings=embeddings,
        segment_count=len(embeddings),
        model=OPENAI_EMBEDDING_MODEL,
    )


def search_translation_memory(
    query: str,
    stored_segments: List[str],
    stored_embeddings: List[List[float]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    client = _get_openai_client()

    query_response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=[query],
        encoding_format="float",
    )
    query_embedding = query_response.data[0].embedding

    results = []
    for idx, stored_embedding in enumerate(stored_embeddings):
        dot_product = sum(a * b for a, b in zip(query_embedding, stored_embedding))
        query_norm = sum(a * a for a in query_embedding) ** 0.5
        stored_norm = sum(a * a for a in stored_embedding) ** 0.5
        if query_norm > 0 and stored_norm > 0:
            similarity = dot_product / (query_norm * stored_norm)
        else:
            similarity = 0.0
        results.append(
            {
                "segment": stored_segments[idx],
                "similarity": similarity,
                "index": idx,
            }
        )

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    req = TranslationMemoryEmbedRequest(
        segments=["Hello world", "Good morning", "Thank you"],
        source_lang="en",
        target_lang="fr",
    )
    resp = embed_translation_segments(req)
    print(f"Embedded {resp.segment_count} segments using {resp.model}")
