import google.generativeai as genai  # Provider-identifying signal
import os


def summarize_asset_content(
    text_content: str,
    model_name: str = "gemini-pro",  # Model family
) -> str:
    """Summarizes content extracted from a stored asset using Google Gemini API."""
    # Assumes GOOGLE_API_KEY is set in environment variables
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel(model_name)
    response = model.generate_content(
        f"Summarize the following content: {text_content}"
    )

    return response.text
