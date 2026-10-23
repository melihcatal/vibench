import os
from google.cloud import aiplatform

def summarize_asset_content(text_content: str) -> str:
    """
    Summarizes content extracted from a stored asset using Google's Gemini Pro model.

    Args:
        text_content: The text content extracted from the asset.

    Returns:
        A summarized version of the text content.
    """
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))

    model = aiplatform.GenerativeModel("gemini-pro")
    
    # Prompt for summarization
    prompt = f"Summarize the following text:

{text_content}"

    response = model.generate_content(prompt)
    
    if response.candidates:
        summary = response.candidates[0].content.parts[0].text
        return summary
    else:
        return "Could not generate summary."

