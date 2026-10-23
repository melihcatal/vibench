import os
from typing import List
from model_client import get_gemini_embedding_model
from model_models import EMBEDDING_001

def get_text_embedding(text: str) -> List[float]:
    """
    Embeds model outputs using Google Gemini Embeddings API.
    """
    embedding_model = get_gemini_embedding_model(EMBEDDING_001)
    response = embedding_model.embed_content(content=text)
    return response['embedding']

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY env var)
    # sample_text = "The quick brown fox jumps over the lazy dog."
    # embedding = get_text_embedding(sample_text)
    # print(f"Embedding length: {len(embedding)}")
    # print(f"First 5 dimensions: {embedding[:5]}")
    pass
