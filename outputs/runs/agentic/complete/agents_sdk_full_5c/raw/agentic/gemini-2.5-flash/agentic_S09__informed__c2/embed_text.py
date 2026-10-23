import os
from embeddings_client import get_gemini_client

def embed_text(text: str, model_name: str = "models/text-embedding-004") -> list[float]:
    """
    Generates an embedding vector for a single text string using Google Gemini Embeddings.
    """
    genai = get_gemini_client()
    response = genai.embed_content(
        model=model_name,
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response['embedding']

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # To run:
    # export GOOGLE_API_KEY='your_api_key_here'
    # python embed_text.py
    sample_text = "The quick brown fox jumps over the lazy dog."
    try:
        embedding = embed_text(sample_text)
        print(f"Embedding for '{sample_text[:30]}...':")
        print(embedding[:5]) # Print first 5 dimensions for brevity
        print(f"Embedding dimension: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
