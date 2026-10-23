import os
from storage_client import get_storage_client
from storage_models import ObjectMetadataResponse
from openai import OpenAI

def embed_asset_metadata(bucket_name: str, object_key: str, model: str = "text-embedding-3-small") -> dict:
    """
    Embeds object metadata and extracted text for search using OpenAI Embeddings.
    Requires OPENAI_API_KEY environment variable.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_key)
    blob.reload()

    metadata_response = ObjectMetadataResponse(
        bucket=bucket_name,
        object_key=object_key,
        size=blob.size,
        content_type=blob.content_type,
        etag=blob.etag,
        last_modified=blob.updated,
        metadata=blob.metadata or {}
    )

    text_content = blob.download_as_text() if blob.size < 1_000_000 else ""
    combined_text = f"Metadata: {metadata_response.metadata}. Content: {text_content}"

    openai_client = OpenAI(api_key=api_key)
    response = openai_client.embeddings.create(
        input=combined_text,
        model=model
    )

    return {
        "embedding": response.data[0].embedding,
        "model": model,
        "input_tokens": response.usage.prompt_tokens
    }