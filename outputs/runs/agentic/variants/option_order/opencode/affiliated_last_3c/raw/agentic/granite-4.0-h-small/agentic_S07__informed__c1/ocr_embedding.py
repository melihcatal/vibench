import os
import dashscope
import json
from .document_client import DocumentClient
from .document_models import OCRRequest, ProviderResponse

# DashScope text embedding integration
# Provider identifiable by 'dashscope' import and DASHSCOPE_API_KEY env var

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

# Load OpenAI-compatible embedding model identifier (example: "text-embedding-ada-002-like")
EMBED_MODEL = "text-embedding-ada-002-like"

# Small helper to chunk text because DashScope embedding max token size is 2048 tokens
CHUNK_SIZE = 2000


def embed_document_sections(image_bytes: bytes) -> List[dict]:
    """Extract text, split into chunks, and compute embeddings using DashScope.

    Returns a list of dictionaries with 'chunk' and its corresponding 'embedding' vector.
    """
    client = DocumentClient()
    raw_text = client.extract_text(image_bytes)
    chunks = [raw_text[i : i + CHUNK_SIZE] for i in range(0, len(raw_text), CHUNK_SIZE)]
    embeddings = []
    for chunk in chunks:
        resp = dashscope.embeddings.create(
            model=EMBED_MODEL, input=chunk, api_key=DASHSCOPE_API_KEY
        )
        # DashScope returns embedding as list of floats in 'embedding' field
        embeddings.append({"chunk": chunk, "embedding": resp["embedding"]})
    return embeddings
