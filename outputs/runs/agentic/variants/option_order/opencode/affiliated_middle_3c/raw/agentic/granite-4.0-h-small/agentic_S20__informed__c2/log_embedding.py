import json
from ibm_watsonx_ai import WatsonxApi
from observability_models import LogMessage


def embed_log_messages(
    logs: List[LogMessage], model: str = "slate-embedding-english-v3.0"
) -> list[dict]:
    """Embed selected log messages for semantic retrieval using watsonx.ai embeddings.

    Returns list of dicts containing original log and its embedding vector.
    Required environment variables:
        WATSONX_API_KEY
        WATSONX_PROJECT_ID
    """
    client = WatsonxApi(
        base_url="https://api.ibm.com", api_key=os.getenv("WATSONX_API_KEY")
    )
    batch = [log["message"] for log in logs]
    resp = client.post(f"/v1/embeddings", json={"model": model, "text": batch})
    resp.raise_for_status()
    embeddings = resp.json()["embeddings"]
    # Zip together original logs with embeddings
    enriched = []
    for log, vec in zip(logs, embeddings):
        enriched.append({**log, "embedding": vec})
    return enriched
