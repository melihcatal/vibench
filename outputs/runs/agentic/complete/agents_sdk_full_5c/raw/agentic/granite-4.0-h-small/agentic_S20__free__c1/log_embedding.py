import json
import time
from observability_models import LogEvent

# Simple utility to synthesize an embedding vector from log message

def log_embedding(log_events: list[LogEvent]) -> list[dict]:
    """Generate dummy embeddings for a list of log events.

    Args:
        log_events (list[LogEvent]): Log entries to embed.

    Returns:
        list[dict]: Each log augmented with a dummy 'embedding' vector.
    """
    enriched = []
    for event in log_events:
        # 768-dimensional placeholder vector
        placeholder = [hash(event['message']) % 1000 / 1000 for _ in range(768)]
        enriched.append({**event, 'embedding': placeholder})
    return enriched
