import os
from openai import OpenAI
from typing import List

def get_text_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generates an embedding for a given text using OpenAI's API.

    Args:
        text: The input string to embed.
        model: The model to use for the embedding.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
        
    client = OpenAI(api_key=api_key)
    
    text_to_embed = text.replace("\n", " ")
    
    try:
        response = client.embeddings.create(input=[text_to_embed], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"An error occurred while generating embedding: {e}")
        return []
