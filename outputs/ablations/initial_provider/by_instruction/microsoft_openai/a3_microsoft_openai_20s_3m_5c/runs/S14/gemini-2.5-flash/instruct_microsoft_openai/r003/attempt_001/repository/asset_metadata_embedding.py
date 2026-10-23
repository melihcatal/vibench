import os
from openai import OpenAI

from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse

def asset_metadata_embedding(request: AssetMetadataEmbeddingRequest) -> AssetMetadataEmbeddingResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    # Combine text content and metadata into a single string for embedding
    metadata_str = " ".join([f"{k}: {v}" for k, v in request.metadata.items()])
    text_to_embed = f"{request.text_content} {metadata_str}".strip()

    if not text_to_embed:
        return AssetMetadataEmbeddingResponse(embedding=[])

    response = client.embeddings.create(
        input=[text_to_embed],
        model="text-embedding-ada-002"  # Concrete model identifier
    )

    embedding = response.data[0].embedding
    return AssetMetadataEmbeddingResponse(embedding=embedding)
