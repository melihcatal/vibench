# transcript_embedding.py
import os
from sentence_transformers import SentenceTransformer, util

# Provider: SentenceTransformer (provider identifiable via model ID)
MODEL_ID = "all-MiniLM-L12-v2"
model = SentenceTransformer(MODEL_ID)


def transcript_embedding(transcript_text: str):
    """Embed transcript segments for semantic retrieval.

    Returns a list of sentence embeddings (float vectors).
    """
    sentences = [seg for seg in transcript_text.split(". ") if seg]
    embeddings = model.encode(sentences, convert_to_tensor=True)
    return embeddings.tolist()
