import cohere
from storage_client import StorageClient
from storage_models import ObjectMetadata


def embed_asset_metadata(metadata: ObjectMetadata, extracted_text: str) -> list[float]:
    """Embed object metadata and extracted text for search using Cohere Embeddings."""
    co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
    
    # Combine metadata and text
    metadata_str = " ".join(f"{k}: {v}" for k, v in metadata["metadata"].items())
    combined_text = f"Metadata: {metadata_str}. Content: {extracted_text}"
    
    # Generate embedding
    response = co.embed(texts=[combined_text], model="embed-english-v3.0")
    return response.embeddings[0]