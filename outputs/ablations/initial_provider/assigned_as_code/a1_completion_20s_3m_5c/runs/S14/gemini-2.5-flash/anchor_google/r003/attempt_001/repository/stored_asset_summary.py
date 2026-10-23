from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse

def summarize_stored_asset(payload: StoredAssetSummaryRequest, config=None):
    config = config or {}
    vertexai.init(project=config["project_id"], location=config.get("region", "us-central1"))
    model = GenerativeModel("gemini-pro") # Using a suitable generative model for summarization

    prompt = f"Summarize the following text:\n\n{payload.text_content}"
    
    response = model.generate_content(prompt)
    summary = response.text

    return StoredAssetSummaryResponse(summary=summary)
