import os
from typing import List
import openai

# Provider: OpenAI
# SDK: openai

def get_text_embedding(text_to_embed: str) -> List[float] | None:
    """
    Generates an embedding for the given text using OpenAI's API.
    Requires OPENAI_API_KEY environment variable.

    :param text_to_embed: The text to generate an embedding for.
    :return: A list of floats representing the embedding, or None on failure.
    """
    if not text_to_embed:
        return None
        
    try:
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        response = client.embeddings.create(
            input=text_to_embed,
            model="text-embedding-3-small"
        )
        
        return response.data[0].embedding
    except Exception as e:
        print(f"An error occurred generating embedding with OpenAI: {e}")
        return None
