import os
import google.generativeai as genai
from typing import List


def embed_transcript_segment(
    segment: str, model_name: str = "embedding-001"
) -> List[float]:
    """Embeds a transcript segment for semantic retrieval using Google Gemini Embeddings.

    Args:
        segment: The text segment to embed.
        model_name: The name of the embedding model to use (default: 'embedding-001').

    Returns:
        A list of floats representing the embedding vector.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    try:
        response = genai.embed_content(model=model_name, content=segment)
        # The embedding is usually in a 'embedding' field within the response dictionary
        if "embedding" in response:
            return response["embedding"]
        else:
            raise ValueError("Embedding not found in the Gemini API response.")
    except Exception as e:
        print(f"Error generating embedding with Gemini API: {e}")
        return []
