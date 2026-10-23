import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def extract_json_from_text(project_id: str, location: str, text: str, model_name: str = "gemini-pro"):
    """
    Calls a hosted LLM to extract structured JSON from text.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region to use (e.g., "us-central1").
        text: The input text from which to extract JSON.
        model_name: The name of the model to use (default: "gemini-pro").

    Returns:
        The extracted JSON as a string, or None if extraction fails.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    
    prompt = f"""
    Extract any structured JSON object from the following text. 
    If no JSON is present, return an empty string.
    
    Text:
    """
    {text}
    """
    
    JSON:
    """
    
    response = model.generate_content(prompt)
    
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    return part.text
    return ""
