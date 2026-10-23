import os
from typing import Dict

from google.cloud import logging_v2

from security_models import build_metadata, normalize_text


def key_usage_summary(project_id: str, query: str) -> Dict[str, object]:
    client = logging_v2.Client(project=project_id)
    entries = list(client.list_entries(filter_=normalize_text(query)))
    return {
        "provider": "google_cloud_logging",
        "count": len(entries),
        "metadata": build_metadata(project_id=project_id, query=query),
    }


def main() -> None:
    project_id = os.getenv("GCP_PROJECT_ID", "")
    query = os.getenv("LOG_QUERY", "resource.type=cloudkms_key")
    print(key_usage_summary(project_id, query))


if __name__ == "__main__":
    main()
