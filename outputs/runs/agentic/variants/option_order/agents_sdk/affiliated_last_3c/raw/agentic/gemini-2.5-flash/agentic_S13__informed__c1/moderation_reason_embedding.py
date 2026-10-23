import os
import google.generativeai as genai
from typing import List

def moderation_reason_embedding(texts: List[str]) -> List[List[float]]:
    """
    Embeds moderation rationales for case retrieval using the Google Gemini Embeddings API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=api_key)

    # The embedding model for Gemini
    EMBEDDING_MODEL = "models/embedding-001"

    try:
        # The `embed_content` method can take a list of texts for batch embedding
        response = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=texts,
            task_type="RETRIEVAL_DOCUMENT" # or other suitable task type
        )
        return [embedding.tolist() for embedding in response["embedding"]]
    except Exception as e:
        raise RuntimeError(f"Error generating embeddings: {e}")

if __name__ == '__main__':
    # Example usage - ensure GOOGLE_API_KEY is set
    # rationales = [
    #     "Content was flagged for hate speech due to derogatory terms.",
    #     "Decision appealed due to misunderstanding of context.",
    #     "Blocked for sexual content as per policy violation."
    # ]
    # try:
    #     embeddings = moderation_reason_embedding(rationales)
    #     print(f"Generated {len(embeddings)} embeddings, each with dimension {len(embeddings[0])}.")
    # except ValueError as e:
    #     print(f"Error: {e}")
    # except RuntimeError as e:
    #     print(f"Runtime Error: {e}")
    pass
