import os
from speech_client import BatchSpeechClient
from speech_models import EmbeddingRequest, EmbeddingResponse
from sentence_transformers import SentenceTransformer

# Local embedding model (example: all-MiniLM-L6-v2)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


def embed_transcript_segments(transcript: str) -> list[EmbeddingResponse]:
    """Embeds each sentence/segment of a transcript for semantic retrieval.

    Args:
        transcript: Full transcript text.

    Returns:
        List of EmbeddingResponse objects, each containing the embedding vector.
    """
    # Simple sentence splitting (period based)
    import re

    segments = [
        seg.strip() for seg in re.split(r"(?<=[.!?]) +", transcript) if seg.strip()
    ]
    embeddings = []
    for seg in segments:
        # Encode segment to embedding vector
        vec = model.encode(seg, convert_to_tensor=True).tolist()
        embeddings.append({"embedding": vec, "text": seg})
    return embeddings
