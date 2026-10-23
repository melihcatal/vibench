import os
from embeddings_client import get_gemini_client

def embed_batch(texts: list[str], model_name: str = "models/text-embedding-004") -> list[list[float]]:
    """
    Generates embedding vectors for a batch of text strings using Google Gemini Embeddings.
    """
    genai = get_gemini_client()
    response = genai.embed_content(
        model=model_name,
        content=texts,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response['embeddings']

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # To run:
    # export GOOGLE_API_KEY='your_api_key_here'
    # python embed_batch.py
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Never underestimate the power of a good book.",
        "Artificial intelligence is transforming industries globally."
    ]
    try:
        embeddings = embed_batch(sample_texts)
        print(f"Embeddings for {len(sample_texts)} texts:")
        for i, emb in enumerate(embeddings):
            print(f"  Text {i+1} embedding (first 5 dim): {emb[:5]}")
            print(f"  Text {i+1} embedding dimension: {len(emb)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
