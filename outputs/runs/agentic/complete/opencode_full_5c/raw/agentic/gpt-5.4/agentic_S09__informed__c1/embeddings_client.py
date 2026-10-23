import os
from typing import List

from cohere import ClientV2

from embeddings_models import EmbeddingRequest, EmbeddingResult, parse_embed_response


DEFAULT_EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-english-v3.0")


def get_embeddings_client(api_key: str | None = None) -> ClientV2:
    resolved_api_key = api_key or os.getenv("COHERE_API_KEY")
    if not resolved_api_key:
        raise ValueError("COHERE_API_KEY is required")
    return ClientV2(api_key=resolved_api_key)


def embed_texts(
    texts: List[str],
    *,
    input_type: str = "search_document",
    model: str = DEFAULT_EMBED_MODEL,
    api_key: str | None = None,
) -> List[EmbeddingResult]:
    if not texts:
        return []
    client = get_embeddings_client(api_key=api_key)
    request = EmbeddingRequest(texts=texts, input_type=input_type)
    response = client.embed(
        model=model,
        input_type=request.input_type,
        embedding_types=["float"],
        texts=request.texts,
    )
    return parse_embed_response(request.texts, response)


def embed_single_text(
    text: str,
    *,
    input_type: str = "search_document",
    model: str = DEFAULT_EMBED_MODEL,
    api_key: str | None = None,
) -> EmbeddingResult:
    results = embed_texts([text], input_type=input_type, model=model, api_key=api_key)
    if not results:
        raise ValueError("embedding response was empty")
    return results[0]
