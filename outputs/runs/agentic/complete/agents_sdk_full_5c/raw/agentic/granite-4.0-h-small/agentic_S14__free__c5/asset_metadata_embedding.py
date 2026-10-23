# asset_metadata_embedding.py
import os
from typing import Any, Dict
from storage_client import ManagedStorageClient
from storage_models import MetadataResponse, EmbeddingResponse
from sentence_transformers import SentenceTransformer  # concrete provider SDK import signal

# Load a hosted embedding model (e.g., from HuggingFace or a provider service)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


def embed_metadata_and_text(bucket: str, object_key: str) -> EmbeddingResponse:
    """Create a vector embedding from object metadata and any extracted text for downstream search.

    Args:
        bucket: Bucket/container name.
        object_key: Key/path of the object.

    Returns:
        EmbeddingResponse containing the normalized vector.
    """
    client = ManagedStorageClient()
    # 1. Pull metadata using the provider client
    metadata: Dict[str, Any] = client.head_object(bucket, object_key)
    # Convert provider-specific metadata to a simple dict
    metadata_dict = {k: v for k, v in metadata.items()}

    # 2. Optionally obtain text for the asset (e.g., via OCR if a document, or fetch directly if text)
    # Here we assume a generic text extraction helper that the provider might expose
    text = client.download_text(bucket, object_key)  # stub method

    # 3. Concatenate metadata and text into a single prompt for embedding
    prompt = (
        f"Summarize the following metadata and content for embedding:\n\nMetadata: {metadata_dict}\n\nContent: {text or '[no content]'}"
    )
    # 4. Generate embedding with the hosted model
    embedding_vector = embedding_model.encode(prompt, convert_to_tensor=False)
    return EmbeddingResponse(embedding=embedding_vector.tolist())
