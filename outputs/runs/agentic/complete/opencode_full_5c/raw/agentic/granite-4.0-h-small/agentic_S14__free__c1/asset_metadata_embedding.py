# asset_metadata_embedding.py
# [LATER-STEP] Embed object metadata and extracted text for vector search
# Using OpenAI Embeddings API as the concrete vector embedding provider
import os
import openai
from storage_models import ObjectMetadataResponse

openai.api_key = os.getenv("OPENAI_API_KEY", "")
client = openai.OpenAI()


def embed_metadata_and_text(metadata: ObjectMetadataResponse, text: str) -> dict:
    """Create an embedding for combined metadata and extracted text.

    Returns a dict containing the embedding vector and related identifiers.
    """
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=f"Metadata: {metadata}\nDocument text: {text}",
    )
    embedding = response.data[0].embedding
    return {
        "embedding": embedding,
        "object_id": metadata.get("object_id", "unknown"),
        "metadata_snapshot": dict(metadata),
        "embedding_timestamp": openai.OpenAI.get_timestamp(),
    }
