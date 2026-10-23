# image_summary.py
# [LATER-STEP] Summarize visual analysis results

from typing import Dict, Any, List
import json


def summarize_analysis(results: Dict[str, Any]) -> str:
    """
    Consolidate results from multiple image analysis steps into a short summary.

    Expected `results` shape (example for Google Vision):
        {
            "labels": [str,...],
            "description": str,
            "text": str,
            "safe": bool
        }

    Args:
        results (Dict[str, Any]): Collected analysis payload.

    Returns:
        str: Human‑readable summary sentence.
    """
    labels = results.get("labels", [])
    description = results.get("description", "no description")
    text = results.get("text", "")
    safe = "safe" if results.get("safe", True) else "potentially unsafe"

    parts = []
    if labels:
        parts.append(f"contains objects: {', '.join(labels)}")
    if description:
        parts.append(f"described as: {description}")
    if text:
        parts.append(f"contains written text: {text}")
    if parts:
        summary = "This image " + " and ".join(parts)
    else:
        summary = "The image appears empty or analysis failed."
    summary += f" {safe} according to policy checks."
    return summary
