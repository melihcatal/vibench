import google.generativeai as genai
import os
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse
from object_metadata import get_object_metadata


def embed_asset_metadata_and_text(
    request: AssetMetadataEmbeddingRequest,
) -> AssetMetadataEmbeddingResponse:
    """Embeds object metadata and extracted text for search using Gemini Embeddings."""
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Get object metadata
    metadata_response = get_object_metadata(request)
    metadata_str = str(metadata_response.metadata)

    # Combine metadata and extracted text
    text_to_embed = f"Metadata: {metadata_str}. Extracted Text: {request.extracted_text if request.extracted_text else ''}"

    model = "models/embedding-001"

    response = genai.embed_content(
        model=model, content=text_to_embed, task_type="RETRIEVAL_DOCUMENT"
    )

    embedding = response["embedding"]

    return AssetMetadataEmbeddingResponse(embedding=embedding)
