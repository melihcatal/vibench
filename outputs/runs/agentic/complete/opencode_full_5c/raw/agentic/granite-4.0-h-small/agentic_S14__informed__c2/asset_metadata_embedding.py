import os
from typing import Dict
from .storage_client import StorageClient
from .storage_models import GenericObjectMetadata


def embed_metadata(
    provider: str, bucket: str, key: str, text: Optional[str] = None
) -> Dict[str, str]:
    """
    Embed object metadata together with optional extracted text for downstream search indexing.

    Returns a dictionary representing the embedding payload (e.g., for a vector store ingest).
    """
    # Fetch existing metadata
    metadata = get_object_metadata(provider, bucket, key)
    payload = {
        "object_id": f"{bucket}/{key}",
        "bucket": bucket,
        "key": key,
        "size": metadata.size,
        "content_type": metadata.content_type or "",
        "last_modified": metadata.last_modified or "",
        "metadata": metadata.extra or {},
    }

    # Optionally include extracted text (e.g., OCR output)
    if text:
        payload["extracted_text"] = text

    # Call Gemini Embeddings API as the example provider
    import google_genai  # type: ignore[import]

    client = google_genai.EmbeddingClient(api_key=os.getenv("GOOGLE_API_KEY"))
    embedding = client.embed_content(
        content=metadata.extra.get(
            "full_text", ""
        ),  # placeholder for actual content if available
        model="gemini-1.5-flash",
    )
    payload["embedding"] = embedding.vector  # vector as list of floats
    return payload

    # If using another embeddings provider, replace the `google_genai.EmbeddingClient`
    # call with the appropriate SDK and method, preserving the same data shape.
