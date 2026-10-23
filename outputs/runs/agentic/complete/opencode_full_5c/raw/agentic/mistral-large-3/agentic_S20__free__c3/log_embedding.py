import os
from typing import List
from observability_client import get_logging_client
from sentence_transformers import SentenceTransformer


def embed_log_messages(log_messages: List[str]) -> List[Dict[str, Any]]:
    """Embed selected log messages for semantic retrieval using Hugging Face's Sentence Transformers."""
    # Load the pre-trained model from Hugging Face
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Generate embeddings for the log messages
    embeddings = model.encode(log_messages, convert_to_tensor=True)

    results = []
    for message, embedding in zip(log_messages, embeddings):
        results.append({"message": message, "embedding": embedding.tolist()})

    return results
