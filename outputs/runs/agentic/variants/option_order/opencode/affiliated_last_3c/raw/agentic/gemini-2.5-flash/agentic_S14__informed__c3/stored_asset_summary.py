import google.generativeai as genai
import os
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse


def summarize_stored_asset(
    request: StoredAssetSummaryRequest,
) -> StoredAssetSummaryResponse:
    """Summarizes content extracted from a stored asset using Google Gemini API."""
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")

    generation_config = {
        "max_output_tokens": request.max_output_tokens
        if request.max_output_tokens
        else 1024,
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
    }

    response = model.generate_content(
        f"Summarize the following text: {request.text_content}",
        generation_config=generation_config,
    )

    summary = response.text

    return StoredAssetSummaryResponse(summary=summary)
