from google.cloud import aiplatform
from typing import Optional
from dataclasses import dataclass

@dataclass
class StoredAssetSummaryRequest:
    text_content: str
    project_id: str
    location: str = "us-central1"

@dataclass
class StoredAssetSummaryResponse:
    summary: str

def summarize_stored_asset_content(request: StoredAssetSummaryRequest) -> StoredAssetSummaryResponse:
    aiplatform.init(project=request.project_id, location=request.location)

    # Using a concrete model ID: text-bison
    # More info: https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models
    parameters = {
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    
    model = aiplatform.PreviewModel.from_pretrained("text-bison") # Provider-identifying signal with model ID
    response = model.predict(request.text_content, **parameters)

    return StoredAssetSummaryResponse(summary=response.text)
