from sentence_transformers import SentenceTransformer
import numpy as np
import os


def embed_log_messages(messages: list) -> list:
    """Embed log messages for semantic retrieval using Sentence Transformers."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(messages, convert_to_numpy=True)
    return embeddings.tolist()