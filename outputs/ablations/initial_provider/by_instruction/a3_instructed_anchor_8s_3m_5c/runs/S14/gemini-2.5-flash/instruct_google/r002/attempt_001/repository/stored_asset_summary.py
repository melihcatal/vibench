import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class StoredAssetSummaryRequest:
    text_content: str
    min_length: int = 50
    max_length: int = 200

@dataclass
class StoredAssetSummaryResponse:
    summary: str
    full_response: Optional[Dict[str, Any]] = None

def summarize_stored_asset_content(request: StoredAssetSummaryRequest) -> StoredAssetSummaryResponse:
    # Initialize Vertex AI (you might want to move this to a central client helper if more Vertex AI calls are made)
    # For this example, assuming project and location are set up in environment or gcloud config
    vertexai.init()
    model = GenerativeModel("gemini-pro") # Using a concrete model identifier

    prompt = f"Summarize the following text, ensuring the summary is between {request.min_length} and {request.max_length} words:\n\n{request.text_content}"

    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 800,
            "temperature": 0.4,
            "top_p": 0.8,
            "top_k": 40
        },
        safety_settings=[] # Adjust as needed
    )

    summary_text = response.text

    return StoredAssetSummaryResponse(summary=summary_text, full_response=response.to_dict())
