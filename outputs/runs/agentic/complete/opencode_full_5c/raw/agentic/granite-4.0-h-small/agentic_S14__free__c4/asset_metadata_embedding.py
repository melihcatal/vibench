import boto3
import openai
from storage_client import get_managed_storage_client
from storage_models import HeadObjectResponse

# Use OpenAI's embeddings API for vector embeddings (managed LLM provider)
openai.api_key = "YOUR_OPENAI_API_KEY"


async def embed_asset_metadata(bucket_name: str, object_key: str) -> dict:
    """Embed object metadata and extracted text for vector search.

    Returns an embedding suitable for similarity search.
    """
    storage_client = get_managed_storage_client()
    # Retrieve object metadata and (example) extracted text placeholder
    metadata = storage_client.head_object(Bucket=bucket_name, Key=object_key)
    # Dummy text extraction - in practice you'd call OCR/OCR pipelines first
    extracted_text = "Example text content extracted from the asset."

    # Combine metadata and text into a single prompt for the embedding model
    prompt = f"Metadata: {metadata}\nContent preview: {extracted_text}"

    embedding = openai.Embedding.create(model="text-embedding-ada-002", input=prompt)[
        "data"
    ][0]["embedding"]
    return {
        "object_key": object_key,
        "embedding": embedding,
        "metadata": metadata.model_dump()
        if hasattr(metadata, "model_dump")
        else metadata,
    }
