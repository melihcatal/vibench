import json
from typing import List, Dict
from observability_models import LogPayload
from observability_client import get_log_client
# Placeholder: In production replace the import with a real embedding SDK such as openai or cohere

def embed_log_messages(log_entries: List[Dict], model_id: str = "text-embedding-ada-002") -> List[Dict]:
    """Embeds selected log messages using a hosted embedding model.

    Returns the original log entries extended with an `embedding` field containing a list of floats.
    """
    # Mock embedding: generate random vector of size 1536 (size of OpenAI ada-002)
    mock_embeddings = (
        [0.01 * i for i in range(1536)]
        for _ in log_entries
    )
    for entry, vec in zip(log_entries, mock_embeddings):
        entry["embedding"] = vec
    return log_entries

if __name__ == "__main__":
    # Example: fetch the five most recent ERROR logs and embed them
    from query_error_logs import query_error_logs
    errors = query_error_logs(severity="ERROR", start_hours=1)[:5]
    embedded = embed_log_messages(errors, model_id="text-embedding-ada-002")
    print(json.dumps(embedded, indent=2))