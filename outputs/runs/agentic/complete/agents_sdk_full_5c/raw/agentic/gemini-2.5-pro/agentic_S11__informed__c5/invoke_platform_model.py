from model_client import get_client
from vertexai.generative_models import GenerativeModel

def invoke_model(prompt: str) -> str:
    """
    Invokes a Google Vertex AI model to generate content.

    Args:
        prompt: The text prompt to send to the model.

    Returns:
        The generated text content from the model.
    """
    get_client()

    # Model name is a provider-specific signal
    model = GenerativeModel("gemini-1.0-pro")

    response = model.generate_content(prompt)
    
    return response.text

