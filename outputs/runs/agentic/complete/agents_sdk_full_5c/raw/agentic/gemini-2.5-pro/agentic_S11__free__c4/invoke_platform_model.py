from model_client import get_cohere_client

def invoke_model(prompt: str) -> str:
    """
    Invokes a Cohere model to get a response for a given prompt.

    Args:
        prompt: The input text prompt.

    Returns:
        The generated text from the model.
    """
    client = get_cohere_client()
    
    response = client.chat(
        model="command-r",
        message=prompt
    )
    
    return response.text
