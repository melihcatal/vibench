from typing import List, Optional

from document_client import get_openai_client
from document_models import EmbeddingResponse

OPENAI_EMBEDDING_MODEL_ID = "text-embedding-3-small"
OPENAI_EMBEDDING_DIMENSIONS = 1536


def embed_ocr_sections(
    sections: List[str],
    model: str = OPENAI_EMBEDDING_MODEL_ID,
    dimensions: int = OPENAI_EMBEDDING_DIMENSIONS,
) -> EmbeddingResponse:
    client = get_openai_client()

    filtered_sections = [s for s in sections if s.strip()]

    if not filtered_sections:
        return EmbeddingResponse(
            embeddings=[],
            section_texts=[],
            model=model,
        )

    response = client.embeddings.create(
        model=model,
        input=filtered_sections,
        dimensions=dimensions,
    )

    embeddings = [item.embedding for item in response.data]

    return EmbeddingResponse(
        embeddings=embeddings,
        section_texts=filtered_sections,
        model=model,
    )


def embed_ocr_lines(
    lines: list,
    model: str = OPENAI_EMBEDDING_MODEL_ID,
    dimensions: int = OPENAI_EMBEDDING_DIMENSIONS,
) -> EmbeddingResponse:
    sections = []
    for line in lines:
        line_text = line.text if hasattr(line, "text") else str(line)
        if line_text.strip():
            sections.append(line_text)

    return embed_ocr_sections(
        sections=sections,
        model=model,
        dimensions=dimensions,
    )


def embed_ocr_blocks(
    blocks: list,
    model: str = OPENAI_EMBEDDING_MODEL_ID,
    dimensions: int = OPENAI_EMBEDDING_DIMENSIONS,
) -> EmbeddingResponse:
    sections = []
    for block in blocks:
        block_text = block.text if hasattr(block, "text") else str(block)
        if block_text.strip():
            sections.append(block_text)

    return embed_ocr_sections(
        sections=sections,
        model=model,
        dimensions=dimensions,
    )


def compute_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embeddings must have the same dimensionality")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = sum(a * a for a in embedding_a) ** 0.5
    norm_b = sum(b * b for b in embedding_b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)
