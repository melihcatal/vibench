import os
from typing import List
import google.generativeai as genai

def moderation_reason_embedding(texts: List[str]) -> List[List[float]]:
    """Embed moderation rationales for case retrieval using Google Gemini Embeddings.

    Args:
        texts: A list of strings representing moderation rationales or related text.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")

    genai.configure(api_key=google_api_key)

    if not texts:
        return []

    try:
        # Gemini Embedding model identifier
        model = "models/embedding-001"
        
        # The embedding model might have limitations on batch size or token count.
        # For simplicity, we process them as a batch here, assuming the input list isn't excessively large.
        response = genai.embed_content(
            model=model,
            content=texts
        )
        
        # The response structure is an EmbedContentResponse, access the embeddings list
        embeddings = [item.values for item in response["embedding"]]
        return embeddings

    except Exception as e:
        print(f"Error generating embeddings with Google Gemini: {e}")
        return []

if __name__ == "__main__":
    # Example usage (requires environment variable GOOGLE_API_KEY)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
    # rationales = [
    #     "Content flagged for severe hate speech.",
    #     "User message contained mild profanity, allowed with warning.",
    #     "Violation of sexual content policy, action taken."
    # ]
    # embeddings = moderation_reason_embedding(rationales)
    # for i, emb in enumerate(embeddings):
    # #   print(f"Embedding for rationale {i}: {emb[:5]}...") # Print first 5 elements for brevity
    #     print(f"Embedding for rationale {i} has length: {len(emb)}")
    pass
