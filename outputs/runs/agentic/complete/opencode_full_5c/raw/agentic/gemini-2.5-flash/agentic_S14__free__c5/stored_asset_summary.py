import os
import google.generativeai as genai
from storage_models import SummarizationRequest, SummarizationResponse


def summarize_stored_asset_content(
    request: SummarizationRequest,
) -> SummarizationResponse:
    # Configure Google Generative AI (Gemini API)
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Select the model for text generation (e.g., gemini-pro)
    model = genai.GenerativeModel("gemini-pro")

    try:
        # Create the prompt for summarization
        prompt = f"Summarize the following text:\n\n{request.text}"

        # Generate content
        response = model.generate_content(prompt)

        # Extract the summarized text
        summary = response.text
        return SummarizationResponse(
            success=True,
            summary=summary,
            message="Content summarized successfully using Google Gemini API.",
        )
    except Exception as e:
        return SummarizationResponse(
            success=False,
            summary=None,
            message=f"Failed to summarize content using Google Gemini API: {str(e)}",
        )
