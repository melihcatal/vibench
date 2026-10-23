import google.generativeai as genai  # Provider-identifying signal
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse
import os


def embed_asset_metadata(
    request: AssetMetadataEmbeddingRequest,
) -> AssetMetadataEmbeddingResponse:
    genai.configure(
        api_key=os.environ.get("GOOGLE_API_KEY")
    )  # Provider-identifying signal

    result = genai.embed_content(
        model=request.model_name,
        content=request.text_content,
        task_type="RETRIEVAL_DOCUMENT",
    )

    return AssetMetadataEmbeddingResponse(embedding=result["embedding"])
