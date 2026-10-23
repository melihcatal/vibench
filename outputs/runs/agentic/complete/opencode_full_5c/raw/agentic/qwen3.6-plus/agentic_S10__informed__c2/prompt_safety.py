import os
from typing import Optional

import requests

from model_models import SafetyResult


def _get_azure_content_safety_config() -> tuple[str, str]:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )
    return endpoint.rstrip("/"), key


def check_text_safety(
    text: str,
    categories: Optional[list[str]] = None,
    threshold: float = 0.5,
) -> SafetyResult:
    endpoint, key = _get_azure_content_safety_config()
    api_version = "2024-02-15-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    body = {"text": text}
    if categories:
        body["categories"] = categories

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()

    category_scores = {}
    flagged = []
    for result in data.get("categoriesAnalysis", []):
        cat = result.get("category", "")
        severity = result.get("severity", 0)
        normalized_score = severity / 7.0 if severity > 0 else 0.0
        category_scores[cat] = normalized_score
        if normalized_score >= threshold:
            flagged.append(cat)

    is_safe = len(flagged) == 0
    return SafetyResult(
        is_safe=is_safe,
        categories=category_scores,
        flagged_categories=flagged,
        raw_response=data,
    )


def check_prompt_safety(
    prompt: str,
    threshold: float = 0.3,
) -> SafetyResult:
    return check_text_safety(
        prompt,
        categories=["Hate", "SelfHarm", "Sexual", "Violence"],
        threshold=threshold,
    )


def check_output_safety(
    output: str,
    threshold: float = 0.5,
) -> SafetyResult:
    return check_text_safety(
        output,
        categories=["Hate", "SelfHarm", "Sexual", "Violence"],
        threshold=threshold,
    )


def check_safety_batch(
    texts: list[str],
    threshold: float = 0.5,
) -> list[SafetyResult]:
    results = []
    for text in texts:
        result = check_text_safety(text, threshold=threshold)
        results.append(result)
    return results
