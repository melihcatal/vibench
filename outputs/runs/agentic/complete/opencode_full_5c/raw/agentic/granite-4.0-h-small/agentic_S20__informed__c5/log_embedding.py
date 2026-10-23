import os
import json
import requests
from observability_client import get_watsonx_api_key, get_watsonx_project_id
from observability_models import LogRecord


def embed_log_records(
    records: list[LogRecord], model: str = "textembedding-3-large"
) -> list[dict]:
    """Embed a batch of LogRecord objects using the watsonx.ai text embeddings API.",
    Returns a list of dictionaries with the original record plus an 'embedding' field.",
    Raises:
        RuntimeError for HTTP errors.",
    """
    endpoint = "https://api.watsonx.ai/ml/v1/text/embeddings"
    api_key = get_watsonx_api_key()
    project_id = get_watsonx_project_id()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "x-watsonx-project": project_id,
    }
    # Combine messages for batch embedding; each record uses its message field.
    texts = [rec.message for rec in records]
    payload = {"model": model, "input": texts}
    resp = requests.post(endpoint, headers=headers, json=payload)
    resp.raise_for_status()
    resp_json = resp.json()
    embeddings = resp_json.get("values", [])
    enriched = []
    for rec, emb in zip(records, embeddings):
        enriched.append(rec.to_dict())
        enriched[-1]["embedding"] = emb  # add embedding vector
    return enriched
