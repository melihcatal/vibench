# asset_metadata_embedding.py
# [LATER-STEP] Embeds object metadata and extracted text for searchable vector search

import json
import numpy as np
from google.cloud import storage, vertexai
from storage_client import ManagedStorageClient
from storage_models import ObjectMetadataResponse

# Example: use Vertex AI's embedding model to create a vector representation
# Vectors can be stored in a vector database (e.g., Elastic, Pinecone) for similarity search


def embed_asset_metadata(bucket_name: str, blob_name: str) -> json:
    """Create embeddings for object metadata and any extracted text.

    Args:
        bucket_name (str): Bucket containing the asset.
        blob_name (str): Object/key of the asset.

    Returns:
        JSON string: Embedding vector and associated metadata.
    """
    client = ManagedStorageClient().get_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Retrieve basic metadata (no download)
    metadata_blob = bucket.get_blob(blob_name, metadata=True)
    meta = {
        "bucket": bucket_name,
        "blob": blob_name,
        "content_type": metadata_blob.content_type,
        "size": metadata_blob.size,
        "created": str(metadata_blob.time_created),
        "updated": str(metadata_blob.time_updated),
    }

    # Retrieve textual content if present (UTF-8 encoding assumed)
    try:
        asset_text = blob.download_as_text()
    except Exception:
        asset_text = ""

    # Initialize Vertex AI embedding model (e.g., textembedding-gecko@003)
    vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location="us-central1")
    embedding_model = vertexai.preview.language_models.EmbeddingModel.from_pretrained(
        "textembedding-gecko@003"
    )

    # Combine metadata JSON and text for embedding
    input_text = json.dumps(meta) + "\n" + asset_text
    embedding = embedding_model.embed_content(input_text)

    # embedding.value is a numpy array of floats (1024 or 1536 dimensions)
    embedding_vector = embedding.value.tolist()

    # Return compact JSON representation
    return json.dumps(
        {"blob_name": blob_name, "embedding": embedding_vector, "metadata": meta},
        indent=2,
    )
