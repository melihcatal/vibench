import os
from openai import OpenAI


def get_script_embedding(script_text: str):
    """
    Generates an embedding for a narration script using OpenAI's API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        input=script_text, model="text-embedding-3-small"
    )

    return response.data[0].embedding
