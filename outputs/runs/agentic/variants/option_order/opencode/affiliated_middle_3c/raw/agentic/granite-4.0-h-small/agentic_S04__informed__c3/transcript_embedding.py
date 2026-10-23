import os
import boto3
from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer
from speech_client import get_speech_client


def embed_segments(transcript_json):
    """Embed transcript segments using a sentence transformer for semantic retrieval.

    Parameters
    ----------
    transcript_json : dict
        Output from a transcription job containing word-level timestamps and text.

    Returns
    -------
    list[tuple]
        Each tuple contains (segment_text, embedding_vector).
    """
    # Extract sentences/segments; simple approach: group words by 5-word windows
    segments = []
    words = [w["word"] for w in transcript_json["results"] if w.get("word")]
    for i in range(0, len(words), 5):
        segment = " ".join(words[i : i + 5])
        segments.append(segment)

    # Initialize model (uses env var MODEL_PATH or default)
    model_name = os.getenv("SENTENCE_EMBED_MODEL", "all-MiniLM-L6-v2")
    model = SentenceTransformer(model_name)
    embeddings = model.encode(segments, show_progress_bar=True)

    return list(zip(segments, embeddings))
