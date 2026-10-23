import google.generativeai as genai
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse
import os

def summarize_stored_asset_content(request: StoredAssetSummaryRequest) -> StoredAssetSummaryResponse:
    """Summarizes content extracted from a stored asset using Google Gemini API."""
    # Assumes GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Using a capable model for summarization

    prompt = f"Please summarize the following text:

{request.text_content}"

    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": request.max_output_tokens,
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1
        }
    )

    # The response might contain parts, join them if necessary
    summary_text = "".join([part.text for part in response.parts])

    return StoredAssetSummaryResponse(
        original_content=request.text_content,
        summary=summary_text
    )
