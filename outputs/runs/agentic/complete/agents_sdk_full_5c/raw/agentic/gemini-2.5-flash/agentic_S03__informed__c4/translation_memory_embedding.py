import google.generativeai as genai
import os
from typing import List

def embed_segments_for_tm(segments: List[str]) -> List[List[float]]:
    """Embeds translated segments for translation-memory search using Gemini Embeddings."""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Using the embedding-001 model for embeddings
    model_name = "models/embedding-001"

    embeddings = []
    for segment in segments:
        try:
            response = genai.embed_content(model=model_name, content=segment, task_type="RETRIEVAL_DOCUMENT")
            embeddings.append(response['embedding'])
        except Exception as e:
            print(f"Error embedding segment '{segment}': {e}")
            embeddings.append([]) # Append empty list or handle error as appropriate

    return embeddings
