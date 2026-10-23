import os
from google.genai import Embedding, ContentReference, HarmBlockThreshold

# Use Gemini embeddings for translation‑memory search
model = "gemini-1.5-flash"


def embed_segments(segments):
    """Embed a list of translated segments for later similarity search.

    Args:
        segments (list[str]): translated text strings.

    Returns:
        list[list[float]]: embedding vectors (one per segment).
    """
    # Gemini does not have a dedicated embeddings endpoint, so we use the chat model
    # to produce embeddings via the `generateContent` call with a system prompt that
    # requests a vector. The response will be a JSON array of numbers.
    # For simplicity we mock the vector here – in production use a dedicated embeddings service.
    mock_vectors = [[0.1 * i + 0.01 for _ in range(768)] for i in range(len(segments))]
    return mock_vectors
