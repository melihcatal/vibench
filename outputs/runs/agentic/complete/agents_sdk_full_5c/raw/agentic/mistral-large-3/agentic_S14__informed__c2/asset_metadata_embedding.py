import os
from typing import Dict, List
from openai import OpenAI
from storage_client import get_b2_client, get_bucket_name
from storage_models import StorageObject


def embed_asset_metadata_and_text(object_name: str) -> Dict:
    b2_api = get_b2_client()
    bucket = b2_api.get_bucket_by_name(get_bucket_name())

    # Get object metadata
    b2_file = bucket.get_file_info_by_name(object_name)
    metadata = b2_file.file_info or {}
    
    # Download the file content
    downloaded_file = bucket.download_file_by_name(object_name)
    content = downloaded_file.download()

    # Extract text based on content type
    text_content = ""
    if b2_file.content_type and b2_file.content_type.startswith("text/"):
        text_content = content.decode('utf-8')
    else:
        text_content = "[Binary or unsupported file type]"

    # Combine metadata and text for embedding
    combined_text = "\n".join([f"{k}: {v}" for k, v in metadata.items()] + [text_content])

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Generate embeddings using OpenAI text-embedding-ada-002
    response = client.embeddings.create(
        input=combined_text,
        model="text-embedding-ada-002"
    )

    return {
        "embedding": response.data[0].embedding,
        "metadata": metadata,
        "text_content_preview": text_content[:200]
    }