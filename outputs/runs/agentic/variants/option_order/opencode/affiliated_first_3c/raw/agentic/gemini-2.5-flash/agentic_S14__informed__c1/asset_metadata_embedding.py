import google.generativeai as genai
import os
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse


def embed_asset_metadata(
    request: AssetMetadataEmbeddingRequest,
) -> AssetMetadataEmbeddingResponse:
    """Embeds object metadata and extracted text for search using Gemini Embeddings."""
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("embedding-001")
    response = model.embed_content(request.text_to_embed)

    return AssetMetadataEmbeddingResponse(embedding=response["embedding"])
