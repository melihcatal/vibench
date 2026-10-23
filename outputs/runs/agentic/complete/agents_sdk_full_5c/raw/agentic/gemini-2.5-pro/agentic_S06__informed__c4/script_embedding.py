import os
from typing import List

from openai import OpenAI


def get_script_embedding(script_text: str) -> List[float]:
    """
    Generates an embedding for a narration script using OpenAI's API.

    The client uses the OPENAI_API_KEY environment variable for authentication.

    Args:
        script_text: The text content of the narration script.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Ensure the input text is not empty and replace newlines
    cleaned_text = script_text.replace("\n", " ")

    model = "text-embedding-3-small"

    response = client.embeddings.create(input=[cleaned_text], model=model)

    if response.data:
        return response.data[0].embedding
    
    return []
