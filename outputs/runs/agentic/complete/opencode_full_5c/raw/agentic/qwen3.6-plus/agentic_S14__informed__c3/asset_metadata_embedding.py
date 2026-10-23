import os
import json
from openai import OpenAI
from storage_client import get_oss_bucket, normalize_object_key
from storage_models import ObjectMetadataResponse


def embed_asset_metadata(
    bucket_name: str,
    object_key: str,
    metadata: dict = None,
    extracted_text: str = None,
    model: str = "text-embedding-3-large",
    dimensions: int = None,
) -> dict:
    object_key = normalize_object_key(object_key)
    bucket = get_oss_bucket(bucket_name)

    if extracted_text is None:
        object_stream = bucket.get_object(object_key)
        document_bytes = object_stream.read()
        extracted_text = document_bytes.decode("utf-8", errors="replace")

    if metadata is None:
        metadata = {
            "object_key": object_key,
            "bucket": bucket_name,
        }

    metadata_json = json.dumps(metadata, sort_keys=True)
    embedding_input = f"Metadata: {metadata_json}\n\nContent: {extracted_text}"

    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    embed_kwargs = {
        "model": model,
        "input": embedding_input,
    }
    if dimensions:
        embed_kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**embed_kwargs)

    embedding_vector = response.data[0].embedding
    usage = response.usage

    return {
        "success": True,
        "object_key": object_key,
        "bucket": bucket_name,
        "model": model,
        "embedding": embedding_vector,
        "embedding_dimension": len(embedding_vector),
        "usage": {
            "prompt_tokens": usage.prompt_tokens,
            "total_tokens": usage.total_tokens,
        },
        "provider": "OpenAI Embeddings",
    }
