from typing import Optional

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from storage_client import get_bucket_name
from storage_models import StoredAssetSummaryPayload, StorageConfig
import os

def stored_asset_summary(payload: StoredAssetSummaryPayload, config: Optional[StorageConfig] = None) -> dict:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if config and config.project_id:
        project_id = config.project_id
    
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided in config or GOOGLE_CLOUD_PROJECT environment variable.")

    vertexai.init(project=project_id, location="us-central1") # Assuming us-central1 for Vertex AI
    model = GenerativeModel("gemini-pro-vision") # Using gemini-pro-vision for image/document understanding
    
    bucket_name = get_bucket_name(config)
    file_uri = f"gs://{bucket_name}/{payload.object_name}"

    # For summarization, we'd typically want to feed the *content* of the asset.
    # As this is a generic asset, we will assume it's a document/image and instruct the model to summarize it.
    # In a real scenario, you might first download and extract text, then pass the text to a text-specific model.
    # However, gemini-pro-vision can handle multi-modal input directly.

    prompt = "Summarize the content of this document or image. Focus on the main topic and key takeaways."
    if payload.max_output_tokens:
        prompt += f" Keep the summary concise, ideally within {payload.max_output_tokens} tokens."

    response = model.generate_content(
        [Part.from_uri(file_uri, mime_type="application/octet-stream"), prompt]
    )

    return {"summary": response.text}
