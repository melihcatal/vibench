"""Check live transcript text for unsafe content using Azure AI Content Safety."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncIterator

import requests

from speech_models import FinalTranscript, PartialTranscript


AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"

AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"

HATE = "Hate"
SELF_HARM = "SelfHarm"
SEXUAL = "Sexual"
VIOLENCE = "Violence"

ALL_CATEGORIES = [HATE, SELF_HARM, SEXUAL, VIOLENCE]


class SafetyLevel(str, Enum):
    """Severity levels returned by Azure AI Content Safety."""
    SAFE = "Safe"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class SafetyAssessment:
    """Result of a content safety check on a transcript segment."""
    text: str
    is_safe: bool
    category_results: dict[str, str] = field(default_factory=dict)
    highest_severity: str = SafetyLevel.SAFE
    raw_response: dict[str, Any] | None = None


def _get_endpoint() -> str:
    """Retrieve the Azure Content Safety endpoint from environment."""
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    if not endpoint:
        raise EnvironmentError(
            f"Environment variable {AZURE_CONTENT_SAFETY_ENDPOINT_ENV} is not set."
        )
    return endpoint.rstrip("/")


def _get_key() -> str:
    """Retrieve the Azure Content Safety key from environment."""
    key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)
    if not key:
        raise EnvironmentError(
            f"Environment variable {AZURE_CONTENT_SAFETY_KEY_ENV} is not set."
        )
    return key


def check_text_safety(
    text: str,
    categories: list[str] | None = None,
    output_type: str = "EightSeverityLevels",
) -> SafetyAssessment:
    """
    Check a text segment for unsafe content using Azure AI Content Safety REST API.

    Parameters
    ----------
    text : str
        The text to analyze.
    categories : list[str] | None
        Categories to check. Defaults to all four categories.
    output_type : str
        "FourSeverityLevels" or "EightSeverityLevels".
    """
    endpoint = _get_endpoint()
    key = _get_key()
    url = f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    payload: dict[str, Any] = {
        "text": text,
        "outputType": output_type,
    }
    if categories:
        payload["categories"] = categories

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    category_results: dict[str, str] = {}
    highest_severity = SafetyLevel.SAFE
    severity_order = [
        SafetyLevel.SAFE,
        SafetyLevel.LOW,
        SafetyLevel.MEDIUM,
        SafetyLevel.HIGH,
    ]

    for cat_result in data.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        if isinstance(severity, int):
            if severity == 0:
                level = SafetyLevel.SAFE
            elif severity <= 2:
                level = SafetyLevel.LOW
            elif severity <= 4:
                level = SafetyLevel.MEDIUM
            else:
                level = SafetyLevel.HIGH
        else:
            level = SafetyLevel(severity) if severity in severity_order else SafetyLevel.SAFE

        category_results[cat_name] = level.value
        if severity_order.index(level) > severity_order.index(SafetyLevel(highest_severity)):
            highest_severity = level

    is_safe = all(
        v in (SafetyLevel.SAFE.value, SafetyLevel.LOW.value)
        for v in category_results.values()
    )

    return SafetyAssessment(
        text=text,
        is_safe=is_safe,
        category_results=category_results,
        highest_severity=highest_severity,
        raw_response=data,
    )


async def monitor_caption_safety(
    captions: AsyncIterator[PartialTranscript | FinalTranscript],
    categories: list[str] | None = None,
    unsafe_callback: callable | None = None,
) -> AsyncIterator[SafetyAssessment]:
    """
    Monitor live captions for unsafe content using Azure AI Content Safety.

    Parameters
    ----------
    captions : AsyncIterator
        Async iterator of PartialTranscript or FinalTranscript.
    categories : list[str] | None
        Categories to monitor. Defaults to all.
    unsafe_callback : callable | None
        Optional callback invoked when unsafe content is detected.
    """
    async for caption in captions:
        text = caption.text
        if not text or text.isspace():
            continue

        assessment = check_text_safety(text, categories=categories)

        if not assessment.is_safe and unsafe_callback:
            unsafe_callback(assessment)

        yield assessment
