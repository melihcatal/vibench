import os
import google.generativeai as genai
from typing import List

def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    """
    Embeds moderation rationales for case retrieval using Google Gemini Embeddings.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Concrete model identifier for embeddings
    embedding_model = "models/embedding-001"

    embeddings = []
    for rationale in rationales:
        response = genai.embed_content(
            model=embedding_model,
            content=rationale,
            task_type="RETRIEVAL_DOCUMENT"
        )
        embeddings.append(response['embedding'])
        
    return embeddings

if __name__ == '__main__':
    # Example usage
    # Set environment variable GOOGLE_API_KEY
    sample_rationales = [
        "This content contains strong hate speech towards a protected group.",
        "The message includes explicit sexual references, violating policy.",
        "User expressed intent for self-harm, requiring immediate attention.",
        "This post is harmless and discusses general topics."
    ]

    try:
        embeddings = embed_moderation_rationales(sample_rationales)
        print(f"Generated {len(embeddings)} embeddings. First embedding snippet: {embeddings[0][:5]}...")
        # In a real scenario, you'd store these embeddings in a vector database
        # and use them for similarity search to retrieve similar cases.
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
