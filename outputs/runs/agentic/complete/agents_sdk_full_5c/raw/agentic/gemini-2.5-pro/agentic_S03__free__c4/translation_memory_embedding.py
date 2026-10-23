from openai import OpenAI
from translation_client import get_openai_api_key
from translation_models import EmbeddingVector

def embed_translation_segment(text: str) -> EmbeddingVector:
    """
    Creates an embedding for a text segment using OpenAI's API.

    Args:
        text: The text to embed.

    Returns:
        An EmbeddingVector containing the numerical vector and model name.
    """
    api_key = get_openai_api_key()
    client = OpenAI(api_key=api_key)
    
    model = "text-embedding-3-small"
    
    response = client.embeddings.create(
        input=[text.replace("\n", " ")],
        model=model
    )
    
    vector = response.data[0].embedding
    
    return EmbeddingVector(vector=vector, model=model)
