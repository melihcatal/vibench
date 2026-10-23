from __future__ import annotations

from openai import OpenAI

from document_models import EmbeddingResult, split_text_into_sections
from document_client import OPENAI_API_KEY, OPENAI_API_BASE, EMBEDDING_MODEL

OPENAI_EMBEDDINGS_ENDPOINT = "https://api.openai.com/v1/embeddings"


def embed_document_sections(
    text: str,
    model: str = EMBEDDING_MODEL,
    api_key: str | None = None,
    api_base: str | None = None,
    max_section_length: int = 1000,
) -> EmbeddingResult:
    key = api_key or OPENAI_API_KEY
    base = api_base or OPENAI_API_BASE

    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    sections = split_text_into_sections(text, max_section_length=max_section_length)

    if not sections:
        return EmbeddingResult(
            embeddings=[],
            section_texts=[],
            model=model,
            total_tokens=0,
        )

    client = OpenAI(api_key=key, base_url=base)

    response = client.embeddings.create(
        model=model,
        input=sections,
    )

    embeddings = []
    total_tokens = 0

    for item in response.data:
        embeddings.append(item.embedding)
        total_tokens += (
            item.get("usage", {}).get("total_tokens", 0) if hasattr(item, "get") else 0
        )

    if hasattr(response, "usage") and response.usage:
        total_tokens = response.usage.total_tokens

    return EmbeddingResult(
        embeddings=embeddings,
        section_texts=sections,
        model=model,
        total_tokens=total_tokens,
    )


def embed_ocr_text(
    ocr_text: str,
    model: str = EMBEDDING_MODEL,
    api_key: str | None = None,
    api_base: str | None = None,
    max_section_length: int = 1000,
) -> EmbeddingResult:
    return embed_document_sections(
        text=ocr_text,
        model=model,
        api_key=api_key,
        api_base=api_base,
        max_section_length=max_section_length,
    )


def embed_single_section(
    text: str,
    model: str = EMBEDDING_MODEL,
    api_key: str | None = None,
    api_base: str | None = None,
) -> list[float]:
    key = api_key or OPENAI_API_KEY
    base = api_base or OPENAI_API_BASE

    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=key, base_url=base)

    response = client.embeddings.create(
        model=model,
        input=text,
    )

    return response.data[0].embedding


def embed_multiple_texts(
    texts: list[str],
    model: str = EMBEDDING_MODEL,
    api_key: str | None = None,
    api_base: str | None = None,
) -> list[list[float]]:
    key = api_key or OPENAI_API_KEY
    base = api_base or OPENAI_API_BASE

    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=key, base_url=base)

    response = client.embeddings.create(
        model=model,
        input=texts,
    )

    return [item.embedding for item in response.data]
