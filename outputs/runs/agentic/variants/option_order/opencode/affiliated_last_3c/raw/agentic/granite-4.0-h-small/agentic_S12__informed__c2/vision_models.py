# vision_models.py
"""Local request/response and normalization helpers for Static Image and Visual Understanding.

These utilities translate between the concrete provider payloads used by vision_client.py
and the higher‑level structures expected by later‑step integration files (summaries,
alternative text, safety text, archival)."

import json
from typing import Any, Dict, List

def normalize_labels(response: Dict[str, Any]) -> List[Dict[str, str]]:
    """Convert provider label payload to a simple list of {name, confidence}."""
    # Expected provider payload: [{"name": "label", "confidence": 0.92}, ...]
    normalized = []
    for item in response.get("labels", []):
        name = item.get("name", "")
        confidence = item.get("confidence")
        normalized.append({"name": name, "confidence": confidence})
    return normalized


def normalize_description(response: Dict[str, Any]) -> str:
    """Extract a concise description string from provider output."""
    # Provider may give multiple description fields; choose the most relevant
    description = response.get("description") or response.get("localizedDescription") or ""
    return description.strip() if description else ""


def normalize_text(response: Dict[str, Any]) -> List[str]:
    """Extract detected text lines from provider output."""
    # Provider may return a list under various keys like "textDetections", "textBlocks"
    text_items = response.get("textDetections", [])
    return [item.get("detectedText", "") for item in text_items]


def normalize_safety(response: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize safety check result to {safe, details}."""
    safe = response.get("safe", True)
    details = response.get("details", [])
    return {
        "safe": safe,
        "details": details
    }


def archive_artifact(artifact_path: str, bucket: str, storage_client) -> str:
    """Archive a local artifact (e.g., JSON result file) to managed object storage.

    Uses a generic storage client interface (e.g., boto3 for S3, or a similar SDK)."
    """
    # Determine file name from path
    filename = os.path.basename(artifact_path)
    # Example: storage_client.upload_file(artifact_path, f"{bucket}/{filename}")
    # For demonstration, return a placeholder URL
    return f"{bucket}/{filename}"
