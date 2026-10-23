import os
import google.generativeai as genai
from typing import List

def embed_transcript_segments(segments_text: List[str]) -> List[List[float]]:
    """
    Embeds transcript segments for semantic retrieval using Google Gemini Embeddings.

    Args:
        segments_text: A list of text strings, where each string is a transcript segment.

    Returns:
        A list of embedding vectors, where each vector corresponds to a segment.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=google_api_key)

    # Using the embedding model specifically for text embedding
    model = 'models/embedding-001'

    try:
        # The embed_content function handles batching internally if multiple items are passed
        response = genai.embed_content(
            model=model,
            content=segments_text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return [embedding.tolist() for embedding in response['embedding']]
    except Exception as e:
        print(f"Error generating embeddings with Gemini API: {e}")
        return []
