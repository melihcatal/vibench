import os
import google.generativeai as genai
from typing import List

def embed_translation_segment(text_segment: str) -> List[float]:
    """Embeds a translated segment for translation-memory search using Gemini Embeddings.

    Args:
        text_segment: The translated text segment to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # The embedding model to use. For general purpose embeddings.
    # Check available models via genai.list_models() and filter for `embedding_model`
    embedding_model = "models/embedding-001"

    response = genai.embed_content(
        model=embedding_model,
        content=text_segment,
        task_type="RETRIEVAL_DOCUMENT" # or RETRIEVAL_QUERY depending on use case
    )

    # The embedding is usually within a 'response.embedding.values' or similar structure.
    # For the `embed_content` function, it returns a dict with 'embedding' key.
    return response['embedding']

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY env var)
    # segment = "This is a translated sentence for embedding."
    # embedding_vector = embed_translation_segment(segment)
    # print(f"Embedding vector length: {len(embedding_vector)}")
    # print(f"First 10 dimensions: {embedding_vector[:10]}")
    pass
