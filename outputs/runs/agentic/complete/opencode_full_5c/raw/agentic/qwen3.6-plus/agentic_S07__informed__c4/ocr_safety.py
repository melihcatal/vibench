import os
import requests
from dataclasses import dataclass, field
from typing import List, Dict, Any


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


@dataclass
class SafetyCategoryResult:
    category: str = ""
    severity: int = 0
    severity_label: str = ""


@dataclass
class SafetyAnalysisResult:
    text: str = ""
    categories: List[SafetyCategoryResult] = field(default_factory=list)
    blocklists_matched: List[Dict[str, Any]] = field(default_factory=list)
    is_safe: bool = True
    highest_severity: int = 0


def analyze_text_safety(text: str) -> SafetyAnalysisResult:
    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "EightSeverityLevels",
    }
    response = requests.post(url, params=params, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()

    categories = []
    highest_severity = 0
    is_safe = True
    for cat_result in data.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        severity_label = cat_result.get("severityLabel", "")
        categories.append(
            SafetyCategoryResult(
                category=cat_name,
                severity=severity,
                severity_label=severity_label,
            )
        )
        if severity > highest_severity:
            highest_severity = severity
        if severity >= 4:
            is_safe = False

    blocklists = data.get("blocklistsMatch", [])

    return SafetyAnalysisResult(
        text=text,
        categories=categories,
        blocklists_matched=blocklists,
        is_safe=is_safe,
        highest_severity=highest_severity,
    )


def analyze_ocr_text_safety(ocr_text: str) -> SafetyAnalysisResult:
    return analyze_text_safety(ocr_text)


def batch_analyze_texts(texts: List[str]) -> List[SafetyAnalysisResult]:
    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "text": "\n".join(texts),
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "EightSeverityLevels",
    }
    response = requests.post(url, params=params, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()

    categories = []
    highest_severity = 0
    is_safe = True
    for cat_result in data.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        severity_label = cat_result.get("severityLabel", "")
        categories.append(
            SafetyCategoryResult(
                category=cat_name,
                severity=severity,
                severity_label=severity_label,
            )
        )
        if severity > highest_severity:
            highest_severity = severity
        if severity >= 4:
            is_safe = False

    return SafetyAnalysisResult(
        text="\n".join(texts),
        categories=categories,
        blocklists_matched=data.get("blocklistsMatch", []),
        is_safe=is_safe,
        highest_severity=highest_severity,
    )
