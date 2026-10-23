import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_text(project_id: str, location: str, text_content: str) -> str:
    """Summarizes long text using a hosted LLM (Google Generative AI).

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        text_content: The long text to summarize.

    Returns:
        The summarized text.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")
    
    prompt = f"""Summarize the following text:
{text_content}
"""
    
    response = model.generate_content(prompt)
    return response.text

