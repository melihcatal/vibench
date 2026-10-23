import os
import requests
from vision_models import VisualAnalysisResult, result_to_dict


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")


def check_visual_safety_text(analysis_result: VisualAnalysisResult) -> dict:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set"
        )
    data = result_to_dict(analysis_result)
    text_to_check = _extract_text_for_moderation(data)
    if not text_to_check.strip():
        return {
            "is_safe": True,
            "categories": {},
            "severity_scores": {},
            "details": "No text content to moderate",
        }
    result = _moderate_text(text_to_check)
    return result


def check_visual_safety_text_from_labels(labels: list[str]) -> dict:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set"
        )
    text_to_check = " ".join(labels)
    if not text_to_check.strip():
        return {
            "is_safe": True,
            "categories": {},
            "severity_scores": {},
            "details": "No text content to moderate",
        }
    result = _moderate_text(text_to_check)
    return result


def _extract_text_for_moderation(data: dict) -> str:
    parts = []
    if data.get("description") and data["description"].get("caption"):
        parts.append(data["description"]["caption"])
    if data.get("detected_text"):
        for t in data["detected_text"]:
            parts.append(t["text"])
    if data.get("labels"):
        for label in data["labels"]:
            parts.append(label["name"])
    return " ".join(parts)


def _moderate_text(text: str) -> dict:
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze"
    params = {"api-version": "2024-02-15-preview"}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }
    response = requests.post(url, params=params, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()
    categories = {}
    severity_scores = {}
    is_safe = True
    for cat_result in data.get("categoriesAnalysis", []):
        category = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        categories[category] = severity > 0
        severity_scores[category] = severity
        if severity >= 4:
            is_safe = False
    return {
        "is_safe": is_safe,
        "categories": categories,
        "severity_scores": severity_scores,
        "details": data.get("blocklistsMatch", []),
    }
