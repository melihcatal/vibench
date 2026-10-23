import os
from typing import List, Dict, Any
from security_client import SecretManagerClient


def secret_label_safety(secret_id: str) -> Dict[str, Any]:
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable must be set.")

    client = SecretManagerClient(project_id=project_id)
    metadata = client.get_secret_metadata(secret_id)

    unsafe_keywords = ["password", "key", "credential", "secret", "token"]
    unsafe_labels = []
    for label_key, label_value in metadata.get("labels", {}).items():
        for keyword in unsafe_keywords:
            if keyword in label_key.lower() or keyword in label_value.lower():
                unsafe_labels.append({label_key: label_value})
                break

    return {
        "secret_id": secret_id,
        "labels": metadata.get("labels"),
        "is_safe": not bool(unsafe_labels),
        "unsafe_labels_found": unsafe_labels,
    }
