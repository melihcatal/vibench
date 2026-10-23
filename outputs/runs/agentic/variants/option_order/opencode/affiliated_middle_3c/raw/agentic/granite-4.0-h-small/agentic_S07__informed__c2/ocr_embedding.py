# ocr_embedding.py
# LATER-STEP file
# Generates embeddings for OCR sections using DashScope Embeddings service

import os
from dashscope.embeddings import text_embedding
from document_models import EmbeddingResult

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise RuntimeError("Set DASHSCOPE_API_KEY for embeddings")


def embed_text_segment(
    text_segment: str, segment_id: str | None = None
) -> EmbeddingResult:
    """Create an embedding vector for a piece of OCR-normalized text.

    Args:
        text_segment: Text chunk to embed (e.g., a paragraph or table cell).
        segment_id: Optional identifier for the segment.

    Returns:
        EmbeddingResult containing the embedding vector and optional segment ID.
    """
    response = text_embedding(text=text_segment, api_key=DASHSCOPE_API_KEY)
    vector = response["embedding"]  # list of floats
    return EmbeddingResult(embedding=vector, segment_id=segment_id)
