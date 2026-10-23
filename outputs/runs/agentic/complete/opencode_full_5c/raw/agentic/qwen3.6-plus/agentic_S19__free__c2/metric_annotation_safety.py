from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import httpx

from observability_models import AnnotationSafetyResult, MetricAnnotation

OPENAI_API_URL = "https://api.openai.com"
OPENAI_MODERATION_ENDPOINT = "/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"
ENV_OPENAI_API_KEY = "OPENAI_API_KEY"


def _get_openai_api_key() -> str:
    api_key = os.environ.get(ENV_OPENAI_API_KEY, "")
    if not api_key:
        raise ValueError(
            f"OpenAI API key is required. Set {ENV_OPENAI_API_KEY} environment variable."
        )
    return api_key


def metric_annotation_safety(
    annotation: MetricAnnotation,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> AnnotationSafetyResult:
    api_key = api_key or _get_openai_api_key()

    text_to_check = annotation.text
    if annotation.labels:
        text_to_check = text_to_check + " " + " ".join(annotation.labels)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "input": text_to_check,
        "model": model,
    }

    response = httpx.post(
        url=f"{OPENAI_API_URL}{OPENAI_MODERATION_ENDPOINT}",
        headers=headers,
        json=payload,
        timeout=15.0,
    )
    response.raise_for_status()
    result_data = response.json()

    results = result_data.get("results", [])
    if not results:
        return AnnotationSafetyResult(
            annotation=annotation,
            is_safe=True,
            safety_score=1.0,
            provider="openai",
            raw_response=result_data,
        )

    moderation_result = results[0]
    flagged = moderation_result.get("flagged", False)
    categories = moderation_result.get("categories", {})
    category_scores = moderation_result.get("category_scores", {})

    flags = []
    flag_details = []
    max_risk_score = 0.0

    for category_name, is_flagged in categories.items():
        if is_flagged:
            flags.append(category_name)
            score = category_scores.get(category_name, 0.0)
            max_risk_score = max(max_risk_score, score)
            flag_details.append(
                {
                    "category": category_name,
                    "flagged": True,
                    "score": score,
                }
            )

    for category_name, score in category_scores.items():
        if category_name not in [fd["category"] for fd in flag_details]:
            flag_details.append(
                {
                    "category": category_name,
                    "flagged": False,
                    "score": score,
                }
            )

    is_safe = not flagged
    safety_score = 1.0 - max_risk_score

    return AnnotationSafetyResult(
        annotation=annotation,
        is_safe=is_safe,
        safety_score=safety_score,
        flags=flags,
        flag_details=flag_details,
        provider="openai",
        raw_response=result_data,
    )


def check_annotation_text_safety(
    text: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> AnnotationSafetyResult:
    annotation = MetricAnnotation(text=text)
    return metric_annotation_safety(annotation=annotation, api_key=api_key, model=model)
