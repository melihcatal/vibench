import google.generativeai as genai
import os
from storage_models import EmbedMetadataRequest, EmbedMetadataResponse


def embed_asset_metadata(request: EmbedMetadataRequest) -> EmbedMetadataResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    text_to_embed = "; ".join([f"{k}: {v}" for k, v in request.metadata_fields.items()])
    if request.text_content:
        text_to_embed += f"; Document Content: {request.text_content}"

    response = genai.embed_content(
        model="models/embedding-001",
        content=text_to_embed,
        task_type="RETRIEVAL_DOCUMENT",
    )

    return EmbedMetadataResponse(embedding=response["embedding"])
