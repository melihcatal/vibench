"""
[LATER-STEP] Embed extracted document sections for semantic retrieval.

Provider: OpenAI Embeddings API
SDK: openai
Auth: OPENAI_API_KEY
Model: text-embedding-ada-002
Service endpoint: api.openai.com
"""

from __future__ import annotations

import os
from typing import Optional, List

from openai import OpenAI

from document_client import get_openai_api_key
from document_models import EmbeddingResult, OcrDocumentResult, LayoutBlock


DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"


def embed_ocr_document(
    ocr_result: OcrDocumentResult,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
) -> EmbeddingResult:
    """
    Generate embeddings for the full plain text of an OCR document using
    OpenAI Embeddings API (api.openai.com) with model text-embedding-ada-002.

    Uses the openai Python SDK.
    """
    api_key = api_key or get_openai_api_key()
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable or api_key argument is required"
        )

    client_kwargs = {"api_key": api_key}
    if organization:
        client_kwargs["organization"] = organization

    client = OpenAI(**client_kwargs)

    text = ocr_result.plain_text
    if not text:
        return EmbeddingResult(model=model, embedding=[], dimension=0)

    response = client.embeddings.create(
        input=text,
        model=model,
    )

    embedding_data = response.data[0]
    embedding = embedding_data.embedding
    dimension = len(embedding)

    return EmbeddingResult(
        text=text,
        model=model,
        embedding=embedding,
        dimension=dimension,
    )


def embed_document_sections(
    ocr_result: OcrDocumentResult,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    batch_size: int = 20,
) -> EmbeddingResult:
    """
    Generate embeddings for individual document sections (layout blocks
    or pages) using OpenAI Embeddings API with model text-embedding-ada-002.

    Returns a parent EmbeddingResult with populated sections list.
    """
    api_key = api_key or get_openai_api_key()
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable or api_key argument is required"
        )

    client = OpenAI(api_key=api_key)

    # Determine sections to embed: layout blocks if available, else lines
    sections_text: List[str] = []
    section_labels: List[str] = []

    if ocr_result.blocks:
        for block in ocr_result.blocks:
            if block.text.strip():
                sections_text.append(block.text.strip())
                section_labels.append(block.block_type)
    elif ocr_result.lines:
        for line in ocr_result.lines:
            if line.text.strip():
                sections_text.append(line.text.strip())
                section_labels.append("line")
    else:
        # Fallback: split plain text into paragraphs
        paragraphs = [p.strip() for p in ocr_result.plain_text.split("\n\n") if p.strip()]
        sections_text = paragraphs
        section_labels = ["paragraph"] * len(paragraphs)

    section_results: List[EmbeddingResult] = []

    for i in range(0, len(sections_text), batch_size):
        batch = sections_text[i : i + batch_size]
        if not batch:
            continue

        response = client.embeddings.create(
            input=batch,
            model=model,
        )

        for idx, emb_data in enumerate(response.data):
            section_results.append(
                EmbeddingResult(
                    text=batch[idx],
                    model=model,
                    embedding=emb_data.embedding,
                    dimension=len(emb_data.embedding),
                )
            )

    return EmbeddingResult(
        text=ocr_result.plain_text,
        model=model,
        embedding=[],
        dimension=section_results[0].dimension if section_results else 0,
        sections=section_results,
    )


def embed_custom_text(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> EmbeddingResult:
    """
    Embed arbitrary text using OpenAI Embeddings API (api.openai.com)
    with the text-embedding-ada-002 model.
    """
    api_key = api_key or get_openai_api_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        input=text,
        model=model,
    )

    emb_data = response.data[0]
    return EmbeddingResult(
        text=text,
        model=model,
        embedding=emb_data.embedding,
        dimension=len(emb_data.embedding),
    )
