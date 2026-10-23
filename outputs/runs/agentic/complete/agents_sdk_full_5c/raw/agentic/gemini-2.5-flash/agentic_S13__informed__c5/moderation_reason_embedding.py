import os
import google.generativeai as genai
from typing import List

def moderation_reason_embedding(rationales: List[str]) -> List[List[float]]:
    """
    Embed moderation rationales for case retrieval using Google Gemini Embeddings.
    """
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=GOOGLE_API_KEY)
    
    embeddings = []
    for rationale in rationales:
        response = genai.embed_content(
            model="models/embedding-001",
            content=rationale,
            task_type="RETRIEVAL_DOCUMENT" # or RETRIEVAL_QUERY depending on use case
        )
        embeddings.append(response['embedding'])
    
    return embeddings

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY to be set)
    # rationales_to_embed = [
    #     "The content contained severe hate speech and incited violence.",
    #     "This message was flagged for explicit sexual content.",
    #     "User posted a message promoting self-harm."
    # ]
    # embedded_vectors = moderation_reason_embedding(rationales_to_embed)
    # print(f"Generated {len(embedded_vectors)} embeddings, each with dimension {len(embedded_vectors[0])}")
    # # print(embedded_vectors[0][:10]) # Print first 10 dimensions of the first embedding
    pass
