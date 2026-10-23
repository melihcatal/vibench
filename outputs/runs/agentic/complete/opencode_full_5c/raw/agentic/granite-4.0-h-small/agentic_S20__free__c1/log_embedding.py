import json
import requests
from observability_client import get_log_service_url, get_auth_header
from observability_models import LogEvent


def embed_log_messages(
    events: List[Dict[str, Any]], model_id: str = "text-embedding-ada-002"
) -> List[Dict[str, Any]]:
    """Embed selected log messages for semantic retrieval.

    Provider: OpenAI Embeddings API (model identifier included).
    """
    url = get_log_service_url() + "/embed"
    headers = {**get_auth_header(), "Content-Type": "application/json"}
    payload = {"events": events, "model": model_id}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json().get("embeddings", [])
