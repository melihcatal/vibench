import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ObservabilityConfig:
    gcp_project_id: str
    gcp_location: str
    gcp_credentials_path: Optional[str]


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        gcp_project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        gcp_location=os.environ.get("GOOGLE_CLOUD_LOCATION", "global"),
        gcp_credentials_path=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
    )


def metric_scope_name(project_id: str) -> str:
    return f"projects/{project_id}"
