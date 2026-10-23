import asyncio
from google.cloud import generativeai as genai
from google.cloud import embedding_retrieval_v1beta as embeddings
from .speech_client import get_google_client
from .speech_models import normalize_google_response, TranscriptEvent

# Embed caption chunks for semantic meeting search using Gemini embeddings.
# Takes streaming transcript events and returns embedding vectors for each chunk.
# Provider identifiers: Google Cloud Speech, Google Gemini embeddings


async def embed_captions(audio_iter=None):
    """
    Streams audio, receives TranscriptEvent objects, creates embeddings for each event text.
    Yields (transcript, embedding) tuples.
    """
    client = get_google_client()  # placeholder for recognition handling
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-mini")  # used for embedding generation
    # Initialize Gemini embeddings client
    em_client = embeddings.EmbeddingRetrievalServiceClient()
    # Define embedding model name (Gemini embedding model)
    embedding_model = (
        "projects/PROJECT_ID/locations/global/publishers/google/models/embed-gemini-1"
    )

    for audio_chunk in audio_iter:
        # Simulated recognition event; replace with actual event handling
        text = "Participants agreed on next steps for the roadmap"  # placeholder
        # Generate embedding (model supports `embed_content` for text embeddings)
        embedding = model.embed_content(text=text)
        # Yield tuple for downstream semantic search
        yield (text, embedding["embedding"])
