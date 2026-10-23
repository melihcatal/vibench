import google.generativeai as genai
import os
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse


def summarize_asset_content(
    request: StoredAssetSummaryRequest,
) -> StoredAssetSummaryResponse:
    """Summarizes content extracted from a stored asset using the Gemini API."""
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(
        f"Summarize the following text: {request.text_content}",
        generation_config={"max_output_tokens": request.max_output_tokens},
    )

    return StoredAssetSummaryResponse(summary=response.text)
