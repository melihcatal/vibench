# HELPER
# Local utilities for request/response normalization and model adapters
import json
from typing import Any, Dict, List


def normalize_labels(raw: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert provider-specific label formats to a common dict."""
    normalized = []
    for lbl in raw:
        normalized.append(
            {
                "name": lbl.get("Name") or lbl.get("description"),
                "confidence": lbl.get("Confidence") or lbl.get("score"),
            }
        )
    return normalized


def normalize_text_blocks(raw: List[Dict[str, Any]]) -> List[str]:
    """Extract just the text strings from text detection responses."""
    return [block.get("Text", "") for block in raw if "Text" in block]


def normalize_moderation(raw: List[Dict[str, Any]]) -> List[str]:
    """Extract unsafe labels."""
    return [label.get("Name") for label in raw if label.get("IsUnsafe", False)]


def summarize_analysis(
    labels: List[str], description: str, texts: List[str], safety: List[str]
) -> str:
    """Create a concise summary report."""
    parts = []
    if labels:
        parts.append(f"Objects detected: {', '.join(labels)}")
    if texts:
        parts.append(f"Text found: {', '.join(texts)}")
    if description:
        parts.append(f"Description: {description}")
    if safety:
        parts.append(f"Unsafe content detected: {', '.join(safety)}")
    return "; ".join(parts) if parts else "No analysis results available."


def save_to_storage(local_path: str, remote_path: str):
    """Placeholder for archiving logic - replace with actual cloud SDK calls."""
    # Example: boto3 client.upload_file(local_path, 'bucket', remote_path)
    print(f"Archiving {local_path} to {remote_path}")
