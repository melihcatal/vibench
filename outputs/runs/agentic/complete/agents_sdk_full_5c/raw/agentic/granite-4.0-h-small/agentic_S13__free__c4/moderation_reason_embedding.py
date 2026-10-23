# moderation_reason_embedding.py
"""Embed moderation rationales for case retrieval using Cohere Rerank model.
"""
import os
import cohere
from safety_models import SafetyResponse

def embed_moderation_rationale(text: str) -> str:
    """Return a concise embedding-friendly representation of the moderation rationale.
    In practice you would call a vector model; here we simply return the flagged categories.
    Environment variable COHERE_API_KEY is required.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("COHERE_API_KEY environment variable not set")
    client = cohere.Client(api_key=api_key)
    # Cohere's Rerank is used here as a stand-in for an embedding endpoint
    response = client.rerank(
        documents=[text],
        query="",
        top_n=1
    )
    # The response's 'rank' field contains the processed text; we extract it
    rationale = response.reranks[0].document  # type: ignore
    return rationale
