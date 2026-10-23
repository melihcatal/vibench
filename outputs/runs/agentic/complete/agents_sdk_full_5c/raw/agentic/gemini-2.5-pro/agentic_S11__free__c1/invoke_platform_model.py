import cohere
from model_client import COHERE_API_KEY

def invoke_model(prompt: str) -> str:
    """
    Invokes a Cohere model to get a direct response.
    """
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(COHERE_API_KEY)

    response = co.chat(
        model="command-r",
        message=prompt,
    )

    return response.text
