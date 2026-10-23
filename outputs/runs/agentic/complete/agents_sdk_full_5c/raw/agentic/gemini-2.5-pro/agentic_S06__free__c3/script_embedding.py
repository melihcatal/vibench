import os
from openai import OpenAI

def get_script_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """
    Generates a vector embedding for a given script using OpenAI's API.

    Requires the OPENAI_API_KEY environment variable to be set.

    Args:
        text: The script text to embed.
        model: The name of the OpenAI embedding model to use.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # OpenAI API expects non-empty input
    text = text.replace("\n", " ")
    if not text:
        raise ValueError("Input text cannot be empty.")

    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding
