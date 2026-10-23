from select_platform_resource import get_model

def invoke_model(prompt: str) -> str:
    """
    Invokes a provider-managed model with a given prompt.

    Args:
        prompt: The input prompt for the model.

    Returns:
        The generated text from the model.
    """
    # The get_model function resolves the specific Google Cloud Vertex AI model
    model = get_model("gemini-1.5-flash-001")
    
    response = model.generate_content(prompt)
    
    return response.text
