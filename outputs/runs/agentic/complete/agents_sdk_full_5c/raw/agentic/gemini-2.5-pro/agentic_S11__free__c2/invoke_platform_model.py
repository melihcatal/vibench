from model_client import get_cohere_client

def invoke_model(prompt: str) -> str:
    """
    Invokes a provider-managed model through a platform client.

    Args:
        prompt: The input prompt for the model.

    Returns:
        The generated text from the model.
    """
    client = get_cohere_client()
    
    # Using a specific Cohere model identifier
    response = client.generate(
        model="command-r",
        prompt=prompt,
        max_tokens=100
    )
    
    return response.generations[0].text
