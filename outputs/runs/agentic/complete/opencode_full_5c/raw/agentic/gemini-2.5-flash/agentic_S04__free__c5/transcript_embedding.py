import os
import sys
import google.generativeai as genai
from typing import List, Dict


def embed_text_segments(text_segments: List[str]) -> List[List[float]]:
    """
    Embeds a list of text segments using Google Generative AI (text-embedding-004).

    Args:
        text_segments: A list of strings, where each string is a transcript segment.

    Returns:
        A list of lists of floats, where each inner list is the embedding vector for a segment.
    """
    # Ensure GOOGLE_API_KEY environment variable is set
    # For example: export GOOGLE_API_KEY="your-api-key"
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = "models/text-embedding-004"  # Using the specific embedding model

    embeddings = []
    print(f"Generating embeddings for {len(text_segments)} segments using {model}...")
    for text in text_segments:
        # The actual embedding generation happens here
        response = genai.embed_content(
            model=model,
            content=text,
            task_type="RETRIEVAL_DOCUMENT",  # Appropriate task type for semantic retrieval
        )
        embeddings.append(response["embedding"])
        print(f"Embedded segment: '{text[:50]}...'")

    return embeddings


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python transcript_embedding.py <text_segment1> [text_segment2 ...]"
        )
        print(
            'Example: python transcript_embedding.py "The quick brown fox" "Jumped over the lazy dog"'
        )
        sys.exit(1)

    text_segments = sys.argv[1:]

    if not text_segments:
        print("No text segments provided for embedding.")
        sys.exit(1)

    try:
        embeddings = embed_text_segments(text_segments)
        print("\n--- Embedding Results (first 5 dimensions of each) ---")
        for i, emb in enumerate(embeddings):
            print(f"Segment {i + 1} (first 5 dims): {emb[:5]}...")
            print(f"  Vector length: {len(emb)}")
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        sys.exit(1)
