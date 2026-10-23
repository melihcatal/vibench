import requests
from security_models import (
    PayloadSafetyRequest,
    PayloadSafetyResponse,
    SafetyCategoryResult,
)
from security_client import load_azure_content_safety_config


def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    config = load_azure_content_safety_config()

    endpoint = config["endpoint"]
    api_key = config["api_key"]

    if not endpoint or not api_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set"
        )

    api_version = "2024-09-01"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    categories = request.categories or [
        "Hate",
        "SelfHarm",
        "Sexual",
        "Violence",
    ]

    body = {
        "text": request.text,
        "categories": categories,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()

    result_data = response.json()

    category_results = []
    max_score = 0.0

    for cat_result in result_data.get("categoriesAnalysis", []):
        category = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        score = severity / 7.0
        flagged = score >= request.threshold

        if score > max_score:
            max_score = score

        category_results.append(
            SafetyCategoryResult(
                category=category,
                score=score,
                flagged=flagged,
            )
        )

    overall_safe = not any(c.flagged for c in category_results)

    return PayloadSafetyResponse(
        safe=overall_safe,
        categories=category_results,
        overall_score=max_score,
        request_id=result_data.get("_metadata", {}).get("requestId", ""),
        metadata={
            "http_status": response.status_code,
            "azure_endpoint": endpoint,
        },
    )
