from typing import Dict
import requests
from observability_client import get_metrics_config

PERSPECTIVE_API = "https://commentanalyzer.googleapis.com"


def metric_annotation_safety(text: str, project_id: str, requested_attributes: Dict[str, float] = None) -> Dict[str, float]:
    cfg = get_metrics_config()
    api_key = cfg.credentials_token
    if not api_key:
        raise ValueError("GOOGLE_OAUTH_ACCESS_TOKEN or GCP_ACCESS_TOKEN is required for Perspective API keyless proxy usage")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": requested_attributes or {"TOXICITY": {}},
    }
    url = f"{PERSPECTIVE_API}/v1alpha1/comments:analyze?key={api_key}"
    resp = requests.post(url, json=payload, timeout=cfg.timeout_seconds)
    resp.raise_for_status()
    data = resp.json()
    return {k: float(v.get("summaryScore", {}).get("value", 0.0)) for k, v in data.get("attributeScores", {}).items()}
