from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


GOOGLE_MONITORING_API = "https://monitoring.googleapis.com/v3"
GOOGLE_CLOUD_STORAGE_API = "https://storage.googleapis.com/storage/v1"
GOOGLE_GEMINI_API = "https://generativelanguage.googleapis.com/v1beta"


def get_gcp_project_id(project_id: Optional[str] = None) -> str:
    resolved = (
        project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    )
    if not resolved:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
    return resolved


def get_google_oauth_token() -> str:
    token = os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN") or os.getenv(
        "GCP_OAUTH_ACCESS_TOKEN"
    )
    if not token:
        raise ValueError(
            "GOOGLE_OAUTH_ACCESS_TOKEN or GCP_OAUTH_ACCESS_TOKEN is required"
        )
    return token


def get_gemini_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY is required")
    return api_key


def monitoring_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {get_google_oauth_token()}",
        "Content-Type": "application/json",
    }


def gcs_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {get_google_oauth_token()}",
        "Content-Type": "application/json",
    }


def fetch_time_series(
    filter_expression: str,
    start_time: str,
    end_time: str,
    project_id: Optional[str] = None,
    alignment_period_seconds: int = 300,
    per_series_aligner: str = "ALIGN_MEAN",
    view: str = "FULL",
) -> Dict[str, Any]:
    project = get_gcp_project_id(project_id)
    params = {
        "filter": filter_expression,
        "interval.startTime": start_time,
        "interval.endTime": end_time,
        "aggregation.alignmentPeriod": f"{alignment_period_seconds}s",
        "aggregation.perSeriesAligner": per_series_aligner,
        "view": view,
    }
    response = requests.get(
        f"{GOOGLE_MONITORING_API}/projects/{project}/timeSeries",
        headers=monitoring_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def upload_json_to_gcs(
    bucket: str, object_name: str, payload: Dict[str, Any]
) -> Dict[str, Any]:
    response = requests.post(
        f"{GOOGLE_CLOUD_STORAGE_API}/b/{bucket}/o",
        headers=gcs_headers(),
        params={"uploadType": "media", "name": object_name},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def gemini_generate(
    model: str, prompt: str, temperature: float = 0.2
) -> Dict[str, Any]:
    response = requests.post(
        f"{GOOGLE_GEMINI_API}/models/{model}:generateContent",
        params={"key": get_gemini_api_key()},
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": temperature},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def extract_gemini_text(payload: Dict[str, Any]) -> str:
    candidates = payload.get("candidates", [])
    if not candidates:
        return ""
    parts = candidates[0].get("content", {}).get("parts", [])
    return "".join(part.get("text", "") for part in parts).strip()
