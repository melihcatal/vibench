from sentence_transformers import SentenceTransformer
from speech_models import TranscriptionResult, TranscriptSegment
from typing import List, Dict
import numpy as np


def transcript_embedding(
    transcript: TranscriptionResult, model_name: str = "all-MiniLM-L6-v2"
) -> Dict[str, List[float]]:
    """
    Embeds transcript segments for semantic retrieval using Sentence Transformers.

    Args:
        transcript: TranscriptionResult containing segments to embed.
        model_name: Pretrained model name from Sentence Transformers (default: "all-MiniLM-L6-v2").

    Returns:
        Dictionary mapping segment indices to their embeddings.
    """
    model = SentenceTransformer(model_name)
    embeddings = {}

    for idx, segment in enumerate(transcript.segments):
        embedding = model.encode(segment.text, convert_to_numpy=True)
        embeddings[idx] = embedding.tolist()

    return embeddings
