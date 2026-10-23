# [LATER-STEP] asset_metadata_embedding.py

# Uses Alibaba Cloud text embeddings to embed object metadata + extracted text for searchable vectors.
# Provider: Alibaba Cloud Text Embedding (DashScope)
# SDK: dashscope
# Auth: DASHSCOPE_API_KEY

import os
import json
from dashscope.text import embed_sentences
from .storage_client import get_bucket_name
from .storage_client import _download_object

# Define a simple normalized payload for embedding
EmbeddedMetadata = dict(
    object_key: str,
    metadata: dict,
    text: str,
    vector: list[float],
)

# Public entry point
async def embed_metadata_and_text(object_key: str, bucket_name: str = None) -> EmbeddedMetadata:
    """Creates a searchable embedding from object metadata and extracted plain text.

    Args:
        object_key: S3 key for the document.
        bucket_name: Optional bucket; defaults to env var.

    Returns:
        dict with `object_key`, `metadata`, `text`, and the `vector` embedding.
    """
    if bucket_name is None:
        bucket_name = get_bucket_name()

    # Grab plain text (could be raw extracted text or combined JSON)
    raw_bytes = _download_object(bucket_name, object_key)
    text = raw_bytes.decode('utf-8')
    # Extract simple metadata from filename & basic S3 info (size, type)
    metadata = {
        'key': object_key,
        'size_bytes': len(raw_bytes),
        'mime_type': 'text/plain',  # placeholder; could be derived from headers
        'last_modified': '2025-01-01T00:00:00Z',  # placeholder
    }
    # Generate embedding (single sentence embedding works for whole document)
    vector = embed_sentences([text], model='embedding_twolyrahuge_base')[0]
    return {
        'object_key': object_key,
        'metadata': metadata,
        'text': text,
        'vector': vector['embeddings'][0],  # list of floats
    }

# Example usage:
# if __name__ == '__main__':
#     print(embed_metadata_and_text('sample.csv'))
