import os
import json
import dashscope

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
dashscope.api_key = DASHSCOPE_API_KEY


def embed_audit_notes(audit_notes: dict) -> str:
    """Embed secret audit notes using DashScope text embeddings for semantic search.
    Returns a JSON string containing the vector representation.
    """
    # Prepare the document text to embed
    text = json.dumps(audit_notes, indent=2)
    response = dashscope.embeddings.create(
        model="qwen2.5-72b-base",
        input=text,
        max_tokens=512,  # typically ignored for embeddings but kept for compatibility
    )
    # The returned embedding is base64 encoded; we keep raw values for downstream use
    embedding = response.embedding  # depends on SDK; assume returns list of floats
    return json.dumps({"vector": embedding, "metadata": audit_notes})
