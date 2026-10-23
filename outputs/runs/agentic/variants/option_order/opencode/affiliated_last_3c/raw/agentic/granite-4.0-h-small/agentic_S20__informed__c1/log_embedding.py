import os
import json
from typing import List
from observability_client import get_embedding_client
from observability_models import LogEvent


def embed_log_messages(
    log_events: List[LogEvent], model: str = "textembedding-gecko@002300"
) -> List[dict]:
    """Embeds selected log messages for semantic retrieval using a hosted embeddings API.

    This implementation uses Google Gemini's embeddings endpoint (identified by the SDK import).
    Returns a list of dicts, each containing the original log event fields plus an 'embedding' key.
    """
    client = get_embedding_client()  # Gemini embeddings client
    # Batch size must respect provider limits (e.g., 1024 tokens per request); split by simple count
    batch_size = 32  # arbitrary safe batch size
    embeddings = []
    for i in range(0, len(log_events), batch_size):
        batch = log_events[i : i + batch_size]
        texts = [f"[{evt['level']}] {evt['message']}" for evt in batch]
        resp = client.embed_content(model=model, content=texts)
        # Expected response: list of vectors + metadata
        for idx, vec in enumerate(resp["embeddings"]):
            orig = batch[idx]
            embeddings.append(
                {
                    "timestamp": orig["timestamp"],
                    "level": orig["level"],
                    "message": orig["message"],
                    "embedding": vec["embedding"],
                }
            )
    return embeddings
