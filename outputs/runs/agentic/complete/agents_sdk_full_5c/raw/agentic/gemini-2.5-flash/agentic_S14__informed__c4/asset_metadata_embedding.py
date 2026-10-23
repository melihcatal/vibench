import google.generativeai as genai
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse
import os

def embed_asset_metadata_and_text(request: AssetMetadataEmbeddingRequest) -> AssetMetadataEmbeddingResponse:
    """Embeds object metadata and extracted text for search using Gemini Embeddings."""
    # Assumes GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Combine text content and metadata into a single string for embedding
    metadata_str = " ".join([f"{k}: {v}" for k, v in request.metadata.items()])
    text_to_embed = f"{request.text_content} {metadata_str}".strip()

    if not text_to_embed:
        raise ValueError("No text content or metadata provided for embedding.")

    embedding_model = 'embedding-001' # A specific model for embeddings

    response = genai.embed_content(
        model=embedding_model,
        content=text_to_embed,
        task_type="RETRIEVAL_DOCUMENT"
    )

    embedding = response['embedding']

    return AssetMetadataEmbeddingResponse(
        text_content=request.text_content,
        embedding=embedding,
        metadata=request.metadata
    )
