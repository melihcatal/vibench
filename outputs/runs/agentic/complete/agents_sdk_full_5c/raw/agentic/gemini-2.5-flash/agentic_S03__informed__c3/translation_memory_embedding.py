import os
import google.generativeai as genai
from typing import List

def embed_text_for_translation_memory(
    text_segments: List[str],
    api_key: str = None,
) -> List[List[float]]:
    """
    Embeds translated text segments for translation-memory search using Google Gemini Embeddings.
    """
    if api_key is None:
        api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    # The embedding-001 model is used for embeddings in the Gemini API.
    # Note: As of my last update, the `embed_content` function is typically used directly
    # with `genai.embed_content` rather than a GenerativeModel instance for embeddings.

    embeddings = []
    for segment in text_segments:
        try:
            # Using genai.embed_content directly for embedding
            # model='embedding-001' is the identifier for the embedding model
            response = genai.embed_content(
                model="models/embedding-001",
                content=segment,
                task_type="RETRIEVAL_DOCUMENT" # or RETRIEVAL_QUERY, SEMANTIC_SIMILARITY, CLASSIFICATION, CLUSTERING
            )
            embeddings.append(response['embedding'])
        except Exception as e:
            print(f"Error embedding segment '{segment}': {e}")
            embeddings.append([]) # Append an empty list or handle error as needed

    return embeddings
