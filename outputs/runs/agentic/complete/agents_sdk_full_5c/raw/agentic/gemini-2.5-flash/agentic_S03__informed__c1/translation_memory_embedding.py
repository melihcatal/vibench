import google.generativeai as genai
import os
from typing import List

def embed_text_for_translation_memory(segment: str) -> List[float]:
    """Embeds a translated segment for translation-memory search using Gemini Embeddings.

    Args:
        segment: The text segment to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # The embedding model to use. For text embedding, 'embedding-001' is a common choice.
    model_name = "models/embedding-001"

    response = genai.embed_content(
        model=model_name,
        content=segment,
        task_type="RETRIEVAL_DOCUMENT"
    )

    return response['embedding']

def embed_batch_for_translation_memory(segments: List[str]) -> List[List[float]]:
    """Embeds a list of translated segments for translation-memory search using Gemini Embeddings.

    Args:
        segments: A list of text segments to embed.

    Returns:
        A list of embedding vectors, one for each segment.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model_name = "models/embedding-001"

    response = genai.embed_content(
        model=model_name,
        content=segments,
        task_type="RETRIEVAL_DOCUMENT"
    )

    return [item['embedding'] for item in response['embeddings']]
