import os
from google.cloud import translate_v2 as translate
from google.cloud import generativemodel

# Local helpers
from translation_client import get_translation_client
from translation_models import validate_language_code, batch_split

MODEL_NAME = "gemini-1.5-pro"  # Explicit model family for embeddings

embed_model = generativemodel.Model(MODEL_NAME)

def embed_translated_segments(segments: list[str], target_lang: str) -> list[list[float]]:
    """Embeds a list of translated text segments for downstream similarity search.

    Args:
        segments: List of translated string fragments.
        target_lang: Target language code (e.g., 'es', 'fr').

    Returns:
        List of embedding vectors (each a list of floats) corresponding to the input order.
    """
    client = get_translation_client()
    validate_language_code(target_lang)
    # Ensure segments are valid non-empty strings
    validated = [validate_text(s) for s in segments]
    # Use Gemini embedding model (supports multilingual)
    responses = embed_model.embed_content(validated, parameters={"temperature": 0})
    # Responses are in the same order as input; each embedding is a list of floats
    return [r.embedding.values for r in responses]

if __name__ == "__main__":
    sample_segments = ["Hello", "How are you?", "Thank you"]
    target = "es"
    embeddings = embed_translated_segments(sample_segments, target)
    print([f"Segment: {s} -> Embedding: {emb[:5]}..." for s, emb in zip(sample_segments, embeddings)])