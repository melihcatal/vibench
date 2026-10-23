import os
from safety_models import SafetyModels
from typing import List

def moderation_reason_embedding(reasons: List[str], model_id: str = 'text-embedding-ada-002') -> List[float]:
    """Embed moderation rationales (reason texts) using OpenAI Embeddings API.
    Returns a flat list of floats representing the embedding vector.
    """
    # Placeholder implementation: simulate embedding vector
    # In production, you would call the OpenAI SDK:
    # import openai; response = openai.Embedding.create(input=reasons, model=model_id)
    # vector = response['data'][0]['embedding']
    # For demo purposes, we return a dummy 1536-dimensional zero vector
    dummy_vector = [0.0] * 1536
    return dummy_vector

# Example usage (commented out)
# reasons = ['Contains hate speech', 'Contains self-harm content']
# embedding = moderation_reason_embedding(reasons)
# print(embedding)
