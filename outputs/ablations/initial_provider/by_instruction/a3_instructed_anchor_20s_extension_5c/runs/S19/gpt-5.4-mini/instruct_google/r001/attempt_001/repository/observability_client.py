import os
from typing import Any, Dict, Optional

import google.auth
from google.auth.transport.requests import AuthorizedSession


def load_google_metrics_session(scopes: Optional[list] = None) -> AuthorizedSession:
    scopes = scopes or ["https://www.googleapis.com/auth/monitoring.read"]
    credentials, _ = google.auth.default(scopes=scopes)
    return AuthorizedSession(credentials)


def load_project_id() -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    return project_id


def google_monitoring_base_url(project_id: str) -> str:
    return f"https://monitoring.googleapis.com/v3/projects/{project_id}"


def post_json(session: AuthorizedSession, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = session.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def get_json(session: AuthorizedSession, url: str) -> Dict[str, Any]:
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
