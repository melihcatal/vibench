import numpy as np
from sentence_transformers import SentenceTransformer
from speech_models import TimestampedTranscriptionResult

def transcript_embedding(segments: list[str]) -> np.ndarray:
    """Embed transcript segments for semantic retrieval using Sentence Transformers."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(segments, convert_to_numpy=True)
    return embeddings