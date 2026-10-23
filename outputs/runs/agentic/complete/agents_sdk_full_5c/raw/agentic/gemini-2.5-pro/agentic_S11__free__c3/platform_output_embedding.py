import os
from typing import List
import openai

def get_openai_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a given text using OpenAI's API.

    Requires the OPENAI_API_KEY environment variable.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
        
    client = openai.OpenAI(api_key=api_key)
    
    # Ensure the text is not empty and replace newlines
    processed_text = text.replace("\n", " ")
    if not processed_text:
        raise ValueError("Input text cannot be empty.")

    response = client.embeddings.create(
        input=[processed_text],
        model="text-embedding-3-small"
    )
    
    return response.data[0].embedding
