import json
from sentence_transformers import SentenceTransformer
from observability_client import get_log_client
from observability_models import LogEvent


def log_embedding(
    logs: list[LogEvent], model_name: str = "all-MiniLM-L6-v2"
) -> list[dict]:
    """Embed selected log messages for semantic retrieval.

    Uses the SentenceTransformer library to compute a dense vector for each message.
    Returns a list of dictionaries containing the original log plus an 'embedding' field.
    """
    model = SentenceTransformer(model_name)
    embedded = []
    for entry in logs:
        vec = model.encode(entry["message"])
        new_entry = entry.copy()
        new_entry["embedding"] = vec.tolist()  # store as list for JSON compatibility
        embedded.append(new_entry)
    return embedded
