import os
from openai import OpenAI

def generate_embedding_openai(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """
    Generates an embedding vector for a single text string using OpenAI.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    try:
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding with OpenAI: {e}")
        return []
