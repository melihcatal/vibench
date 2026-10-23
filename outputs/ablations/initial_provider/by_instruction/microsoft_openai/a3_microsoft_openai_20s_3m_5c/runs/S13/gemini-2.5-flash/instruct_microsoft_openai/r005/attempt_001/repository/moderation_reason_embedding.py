import os
import google.generativeai as genai
from typing import List

def moderation_reason_embedding(rationales: List[str]) -> List[List[float]]:
    """
    Embed moderation rationales for case retrieval using Google's Generative AI embedding models.
    """
    # Ensure GOOGLE_API_KEY environment variable is set.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    try:
        # Using an embedding model available through Google's Generative AI
        # For example, 'models/embedding-001'
        model = "models/text-embedding-004"
        
        # The API expects a list of texts for batch embedding
        # Each item in `rationales` will be embedded individually
        embeddings = []
        for rationale in rationales:
            response = genai.embed_content(
                model=model,
                content=rationale,
                task_type="RETRIEVAL_DOCUMENT"
            )
            embeddings.append(response['embedding'])
        
        return embeddings

    except Exception as e:
        print(f"Error embedding moderation rationales: {str(e)}")
        return []

if __name__ == "__main__":
    # Example Usage
    # Set GOOGLE_API_KEY environment variable.
    # export GOOGLE_API_KEY="your-api-key"
    sample_rationales = [
        "The text contained hate speech and incited violence.",
        "This message was identified as self-harm content with high severity.",
        "No policy violations were found in the submitted text."
    ]
    embeddings = moderation_reason_embedding(sample_rationales)
    if embeddings:
        for i, embedding in enumerate(embeddings):
            print(f"Embedding for rationale {i+1} (first 5 values): {embedding[:5]}...")
