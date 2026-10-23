from typing import Dict, Optional
import base64
import json
import requests
from observability_client import get_metrics_config

GCS_UPLOAD_HOST = "https://storage.googleapis.com"


def metrics_export_archive(bucket_name: str, object_name: str, snapshot: Dict, content_type: str = "application/json") -> Dict[str, str]:
    cfg = get_metrics_config()
    token = cfg.credentials_token
    if not token:
        raise ValueError("GOOGLE_OAUTH_ACCESS_TOKEN or GCP_ACCESS_TOKEN is required for Google Cloud Storage")
    url = f"{GCS_UPLOAD_HOST}/upload/storage/v1/b/{bucket_name}/o"
    params = {"uploadType": "media", "name": object_name}
    headers = {"Authorization": f"Bearer {token}", "Content-Type": content_type}
    payload = json.dumps(snapshot).encode("utf-8")
    resp = requests.post(url, headers=headers, params=params, data=payload, timeout=cfg.timeout_seconds)
    resp.raise_for_status()
    data = resp.json()
    return {"bucket": bucket_name, "object": data.get("name", object_name), "generation": str(data.get("generation", ""))}
