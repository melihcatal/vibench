import os
from observability_client import get_ingestion_client
from observability_models import LogEvent
import dashscope


def embed_log_messages(events: list[LogEvent], model: str = "qwen2") -> list[LogEvent]:
    """Embeds selected log messages for semantic retrieval.

    Uses DashScope Qwen embeddings as an example. Adds a new field `embedding`
    containing a list of floats to each event and returns the updated events.
    """
    client = get_ingestion_client()  # placeholder – embedding done locally
    embedded_events = []
    for evt in events:
        text = evt["message"]
        # DashScope embedding call (synchronous)
        embedding = dashscope.embeddings.create(
            model=model,
            input=text,
        )
        # The response format is provider‑specific; assume list of floats
        embedding_vector = embedding["embedding"]
        new_evt = evt.copy()
        new_evt["embedding"] = embedding_vector
        embedded_events.append(new_evt)
    return embedded_events
