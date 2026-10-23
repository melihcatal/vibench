
from google.cloud import aiplatform

def summarize_text(project_id: str, location: str, text_content: str) -> str:
    """Summarizes content extracted from a stored asset using Google Cloud Vertex AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region to use (e.g., "us-central1").
        text_content: The text content to summarize.

    Returns:
        The summarized text.
    """
    aiplatform.init(project=project_id, location=location)

    # Use a specific model, e.g., "gemini-pro"
    model = aiplatform.GenerativeModel("gemini-pro")
    
    # Define the prompt for summarization
    prompt = f"Summarize the following text:

{text_content}"

    response = model.generate_content(prompt)
    
    if response.candidates:
        return response.candidates[0].content.text
    else:
        return "No summary could be generated."

