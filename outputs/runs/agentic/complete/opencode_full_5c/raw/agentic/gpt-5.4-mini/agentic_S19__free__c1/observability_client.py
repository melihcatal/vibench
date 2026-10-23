import os
from datetime import datetime
from typing import Any, Dict, Optional

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

from observability_models import to_iso8601


class ManagedMetricsClient:
    def __init__(
        self,
        project_id: str,
        location: str = "global",
        credential_file: Optional[str] = None,
    ):
        self.project_id = project_id
        self.location = location
        self.base_url = f"https://monitoring.googleapis.com/v3/projects/{project_id}"
        self.session = self._build_session(credential_file)

    def _build_session(self, credential_file: Optional[str]):
        credential_file = credential_file or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        if credential_file:
            credentials = service_account.Credentials.from_service_account_file(
                credential_file,
                scopes=["https://www.googleapis.com/auth/monitoring.read"],
            )
            return AuthorizedSession(credentials)
        return AuthorizedSession(None)

    def query_time_series(
        self,
        metric_type: str,
        start_time: datetime,
        end_time: datetime,
        filter_expression: str,
        view: str = "FULL",
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/timeSeries"
        params = {
            "filter": filter_expression,
            "interval.startTime": to_iso8601(start_time),
            "interval.endTime": to_iso8601(end_time),
            "view": view,
        }
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def list_time_series(self, request_body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/timeSeries:list"
        response = self.session.post(url, json=request_body, timeout=30)
        response.raise_for_status()
        return response.json()

    def create_metric_descriptor(self, body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/metricDescriptors"
        response = self.session.post(url, json=body, timeout=30)
        response.raise_for_status()
        return response.json()
