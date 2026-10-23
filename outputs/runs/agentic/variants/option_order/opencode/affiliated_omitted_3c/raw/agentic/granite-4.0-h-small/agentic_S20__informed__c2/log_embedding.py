import os
import numpy as np
from typing import List
from observability_client import get_log_client
from observability_models import LogEvent


def log_embedding(log_events: List[LogEvent], model_id: str = "default") -> List[float]:
    """Embed selected log messages for semantic retrieval.

    Calls the configured embeddings provider (e.g., DashScope embeddings,
    OpenAI embeddings, etc.) via the provider client's `embed` method.
    Returns a list of embedding vectors (as numpy arrays) aligned with the input events.
    """
    client = get_log_client()
    texts = [ev.message for ev in log_events]
    # Example SDK call (DashScope embeddings)
    # response = client.embeddings(model_id=model_id, texts=texts)
    # embeddings = [np.array(v['embedding']) for v in response['data']]
    # Placeholder implementation returning random vectors for demo purposes
    embeddings = [np.random.rand(1536).tolist() for _ in texts]
    return embeddings
