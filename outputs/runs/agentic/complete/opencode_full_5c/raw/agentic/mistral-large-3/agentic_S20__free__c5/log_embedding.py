from typing import List
from sentence_transformers import SentenceTransformer


def embed_log_messages(log_messages: List[str]) -> List[dict]:
    """Embed log messages for semantic retrieval using Sentence Transformers."""
    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(log_messages, convert_to_tensor=False)

    results = []
    for message, embedding in zip(log_messages, embeddings):
        results.append({"message": message, "embedding": embedding.tolist()})

    return results
