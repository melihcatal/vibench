import os
from typing import List
import google.generativeai as genai
from safety_client import get_generative_ai_client # To ensure provider signal linkage
from safety_models import EmbeddingRequest, EmbeddingResult

def embed_moderation_rationales(rationales: List[str]) -> List[EmbeddingResult]:
    """
    Embeds moderation rationales for case retrieval using Google Generative AI embedding models.
    """
    genai_client = get_generative_ai_client()
    
    # Specify the embedding model, e.g., 'embedding-001'
    model_name = "models/embedding-001" 

    embeddings = []
    for rationale_text in rationales:
        response = genai_client.embed_content(
            model=model_name,
            content=rationale_text
        )
        embeddings.append(EmbeddingResult(embedding=response['embedding']))
    
    return embeddings

if __name__ == '__main__':
    # Example usage:
    # Ensure GEMINI_API_KEY (or GOOGLE_API_KEY) is set in your environment
    # reasons = [
    #     "The content contained severe toxicity and hate speech.",
    #     "This comment was flagged for profanity but deemed acceptable after review.",
    #     "User appealed the decision for identity attack."
    # ]
    # embedded_rationales = embed_moderation_rationales(reasons)
    # for i, embedding in enumerate(embedded_rationales):
    #     print(f"Rationale {i+1} embedding length: {len(embedding.embedding)}")
    #     print(f"First 5 dimensions: {embedding.embedding[:5]}")
    pass
