from typing import List, Dict
import os
import cohere


def embed_log_messages(messages: List[str]) -> List[Dict[str, List[float]]]:
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(texts=messages, model="embed-english-v3.0")
    return [{"message": msg, "embedding": embedding} for msg, embedding in zip(messages, response.embeddings)]}âgewrite_file Republike{