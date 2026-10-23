import google.generativeai as genai # Provider-identifying signal
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse
import os

def summarize_stored_asset(request: StoredAssetSummaryRequest) -> StoredAssetSummaryResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY")) # Provider-identifying signal

    model = genai.GenerativeModel(request.model_name)

    response = model.generate_content(
        f"Summarize the following text:
\n{request.text_content}"
    )

    return StoredAssetSummaryResponse(summary=response.text)
