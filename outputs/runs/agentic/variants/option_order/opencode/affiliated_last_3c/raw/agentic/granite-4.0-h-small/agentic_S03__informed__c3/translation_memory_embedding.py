import os

try:
    from google.cloud import generativeai as genai
    from google.cloud.generativeml.embedding import EmbeddingModel
except ImportError:
    raise ImportError("Install Vertex AI SDK: pip install google-cloud-aiplatform")

# Load API key from environment (Google)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Set the GOOGLE_API_KEY environment variable")

# Configure Gemini model for embeddings (used for translation-memory search)
genai.configure(api_key=GOOGLE_API_KEY)
EMBED_MODEL = EmbeddingModel(
    "gemini-1.5-flash"
)  # or any Gemini model supporting embeddings


def embed_translated_segments(segments: list[str]) -> list[list[float]]:
    """Embed translated segments for translation-memory search using Gemini.

    Args:
        segments (list[str]): List of translated text segments.

    Returns:
        list[list[float]]: List of embedding vectors (one per segment).
    """
    embeddings = []
    for seg in segments:
        resp = EMBED_MODEL.embed_content(content=seg, temperature=0)
        # Response contains list of embedding vectors; take first (and only)
        embeddings.append(resp.embeddings[0].embedding)
    return embeddings
