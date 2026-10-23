import json
import os
from openai import OpenAI
from typing import Dict, Any


def embed_asset_metadata_and_text(
    bucket_name: str, object_key: str, text: str
) -> Dict[str, Any]:
    """Create an embedding of combined metadata and extracted text using the OpenAI Embeddings API.

    Provider: OpenAI Embeddings (openai SDK).
    API key via OPENAI_API_KEY env var. Model defaults to text-embedding-3-large.
    Returns the embedding vector and related metadata.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    combined_input = json.dumps(
        {
            "bucket": bucket_name,
            "key": object_key,
            "metadata": {
                "size": 0,  # placeholder; replace with real metadata if needed
                "last_modified": "",
                "type": "document",
            },
            "extracted_text": text,
        }
    )
    try:
        resp = client.embeddings.create(
            model="text-embedding-3-large", input=combined_input
        )
        embedding = resp.data[0].embedding  # type: ignore
        return {
            "bucket": bucket_name,
            "key": object_key,
            "embedding": embedding,
            "text_length": len(text),
        }
    except Exception as e:
        raise RuntimeError(f"Embedding creation failed: {e}")

    print("Embedding of asset metadata and text completed")
