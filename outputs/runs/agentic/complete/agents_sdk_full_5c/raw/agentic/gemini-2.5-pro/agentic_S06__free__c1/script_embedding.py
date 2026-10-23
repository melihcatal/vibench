import os
from typing import List
from openai import OpenAI

def get_script_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generates an embedding for a narration script using the OpenAI API.

    Args:
        text: The script content to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    text = text.replace("\\n", " ")
    
    try:
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding with OpenAI: {e}")
        raise
