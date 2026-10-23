import vertexai
from vertexai.generative_models import GenerativeModel, Part

def collect_platform_metadata(project_id: str, location: str, prompt: str):
    """
    Returns model output together with provider platform metadata.
    Uses Google Cloud Vertex AI 'gemini-pro' model.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")
    
    response = model.generate_content(prompt)
    
    metadata = {
        "model_name": "gemini-pro",
        "provider": "Google Cloud Vertex AI",
        "prompt_token_count": response.usage_metadata.prompt_token_count,
        "candidates_token_count": response.usage_metadata.candidates_token_count,
        "total_token_count": response.usage_metadata.total_token_count,
    }
    
    return response.text, metadata

