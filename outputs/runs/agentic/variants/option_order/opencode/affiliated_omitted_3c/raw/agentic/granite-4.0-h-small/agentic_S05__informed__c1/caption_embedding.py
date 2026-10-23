# LATER-STEP: caption_embedding.py
# Embed caption chunks for semantic meeting search

import asyncio
import json
from sentence_transformers import (
    SentenceTransformer,
)  # pip install sentence-transformers
from speech_models import TranscriptionResult, normalize_message

# Load a lightweight embedding model (e.g., all-MiniLM-L6-v2)
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


async def embed_captions(stream_source: str, provider: str = "deepgram"):
    """Stream audio, transcribe, and yield embedding vectors for each final caption.

    Args:
        stream_source: Audio source (WebSocket URL, file path, etc.).
        provider: Speech‑to‑Text provider to use.
    Yields:
        tuple: (embedding vector, original text)
    """
    async for result in _simulate_stream_provider(provider, stream_source):
        if result.is_final:
            embeddings = EMBED_MODEL.encode(result.text, convert_to_tensor=True)
            print(f"[EMBED] text='{result.text}' shape={embeddings.shape}")
            yield embeddings, result.text


async def _simulate_stream_provider(provider: str, source: str):
    """Placeholder async generator mimicking live streaming.
    Replace with real streaming implementation.
    """
    dummy_chunks = [
        TranscriptionResult(text="We need to improve onboarding.", is_final=True),
        TranscriptionResult(
            text="Feature X will be released next week.", is_final=True
        ),
        TranscriptionResult(
            text="Feedback suggests UI changes are welcome.", is_final=True
        ),
    ]
    for chunk in dummy_chunks:
        yield chunk


if __name__ == "__main__":
    # Example usage with Deepgram streaming (replace URL with real endpoint)
    asyncio.run(embed_captions("wss://example.com/stream", provider="deepgram"))
