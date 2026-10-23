import os
from typing import Optional
from dataclasses import dataclass
from enum import Enum

import requests

from speech_models import StreamingRecognitionResult, normalize_transcript_text


AZURE_CONTENT_SAFETY_ENDPOINT_DEFAULT = (
    "https://<your-resource>.cognitiveservices.azure.com/"
)
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


class SafetyCategory(str, Enum):
    HATE = "Hate"
    SELF_HARM = "SelfHarm"
    SEXUAL = "Sexual"
    VIOLENCE = "Violence"


class SeverityLevel(str, Enum):
    SAFE = "Safe"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class SafetyAssessment:
    text: str
    is_safe: bool
    categories: dict[str, SeverityLevel]
    highest_severity: SeverityLevel
    flagged_categories: list[str]
    raw_response: dict


def load_azure_content_safety_config() -> tuple[str, str]:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required for Azure AI Content Safety"
        )
    return endpoint.rstrip("/"), key


def analyze_text_safety(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    categories: Optional[list[str]] = None,
    output_type: str = "FourSeverityLevels",
) -> SafetyAssessment:
    if endpoint is None or api_key is None:
        endpoint, api_key = load_azure_content_safety_config()

    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    body = {"text": text, "outputType": output_type}
    if categories:
        body["categories"] = categories

    response = requests.post(url, headers=headers, params=params, json=body)
    response.raise_for_status()
    data = response.json()

    category_results = {}
    flagged = []
    max_severity = SeverityLevel.SAFE

    severity_order = {
        SeverityLevel.SAFE: 0,
        SeverityLevel.LOW: 1,
        SeverityLevel.MEDIUM: 2,
        SeverityLevel.HIGH: 3,
    }

    for cat_result in data.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "")
        severity_val = cat_result.get("severity", 0)

        if severity_val == 0:
            level = SeverityLevel.SAFE
        elif severity_val <= 2:
            level = SeverityLevel.LOW
        elif severity_val <= 4:
            level = SeverityLevel.MEDIUM
        else:
            level = SeverityLevel.HIGH

        category_results[cat_name] = level
        if level != SeverityLevel.SAFE:
            flagged.append(cat_name)
        if severity_order.get(level, 0) > severity_order.get(max_severity, 0):
            max_severity = level

    return SafetyAssessment(
        text=text,
        is_safe=len(flagged) == 0,
        categories=category_results,
        highest_severity=max_severity,
        flagged_categories=flagged,
        raw_response=data,
    )


async def check_live_caption_safety(
    caption: StreamingRecognitionResult,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    threshold: SeverityLevel = SeverityLevel.MEDIUM,
) -> Optional[SafetyAssessment]:
    if not caption.is_final or not caption.text.strip():
        return None

    normalized = normalize_transcript_text(caption)
    assessment = analyze_text_safety(
        text=normalized,
        endpoint=endpoint,
        api_key=api_key,
    )

    severity_order = {
        SeverityLevel.SAFE: 0,
        SeverityLevel.LOW: 1,
        SeverityLevel.MEDIUM: 2,
        SeverityLevel.HIGH: 3,
    }

    if severity_order.get(assessment.highest_severity, 0) >= severity_order.get(
        threshold, 0
    ):
        return assessment

    return None


async def screen_caption_stream(
    caption_stream,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    threshold: SeverityLevel = SeverityLevel.LOW,
):
    async for caption in caption_stream:
        assessment = await check_live_caption_safety(
            caption=caption,
            endpoint=endpoint,
            api_key=api_key,
            threshold=threshold,
        )
        if assessment is not None:
            yield assessment
