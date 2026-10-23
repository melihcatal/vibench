import json
from typing import Dict, List, Optional
from storage_client import ManagedClient
from storage_models import ObjectInfo, EmbeddingVector, AssetSummary
from typing import Any

# Assume OpenAI embeddings SDK is installed (pip install openai)
import openai


def embed_metadata_and_text(asset: AssetSummary) -> Dict[str, Any]:
    """Embed object metadata and extracted text for downstream vector search.

    The function combines:
    * Basic metadata (bucket, key, size, last_modified)
    * The summarized text produced by `stored_asset_summary`
    * Any additional custom metadata stored in the object's user‑metadata (if present)

    It calls the OpenAI Embeddings API to obtain a vector representation and returns
    a dictionary ready to be stored in a vector store.

    OpenAI credentials are read from environment variable OPENAI_API_KEY.
    """
    # 1. Assemble the textual representation
    description = f"Object key: {asset.metadata['object_key']}\nBucket: {asset.metadata['bucket']}\n"
    description += f"Size: {asset.metadata.get('size_bytes')} bytes\n"
    description += f"Last modified: {asset.metadata.get('last_modified')}\n"
    # Include any custom user metadata that the object may have
    client = ManagedClient()
    obj = client.head_object(asset.metadata["bucket"], asset.metadata["object_key"])
    user_meta = obj.get("UserMetadata", {})
    description += "User metadata:\n"
    for k, v in user_meta.items():
        description += f"  {k}: {v}\n"
    description += "\n" + asset.summary  # the concise human‑readable summary

    # 2. Call the embeddings endpoint
    response = openai.Embedding.create(
        model="text-embedding-ada-002", input=description
    )
    embedding = response["data"][0]["embedding"]
    # 3. Return a serialisable dict
    return {
        "id": asset.metadata["object_key"],
        "bucket": asset.metadata["bucket"],
        "embedding": embedding,
        "metadata": asset.metadata,
        "summary": asset.summary,
    }
