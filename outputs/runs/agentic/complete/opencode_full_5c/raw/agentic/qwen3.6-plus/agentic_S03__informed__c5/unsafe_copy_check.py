import os
import requests
from typing import List, Dict, Any, Optional
from translation_models import UnsafeCopyCheckRequest, UnsafeCopyCheckResponse

AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"
AZURE_CONTENT_SAFETY_ANALYZE_URL = "/contentsafety/text:analyze?api-version={}"

DEFAULT_CATEGORIES = ["Hate", "SelfHarm", "Sexual", "Violence"]


def _get_azure_content_safety_config() -> Dict[str, str]:
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)
    if not endpoint or not key:
        raise ValueError(
            f"Azure Content Safety credentials not found. Set {AZURE_CONTENT_SAFETY_ENDPOINT_ENV} and {AZURE_CONTENT_SAFETY_KEY_ENV}."
        )
    return {"endpoint": endpoint.rstrip("/"), "key": key}


def check_unsafe_copy(request: UnsafeCopyCheckRequest) -> UnsafeCopyCheckResponse:
    config = _get_azure_content_safety_config()
    categories = request.categories or DEFAULT_CATEGORIES

    url = f"{config['endpoint']}{AZURE_CONTENT_SAFETY_ANALYZE_URL.format(AZURE_CONTENT_SAFETY_API_VERSION)}"
    headers = {
        "Ocp-Apim-Subscription-Key": config["key"],
        "Content-Type": "application/json",
    }

    text_categories = [{"category": cat} for cat in categories]

    payload = {
        "text": request.text,
        "categories": text_categories,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    flagged_categories = []
    details = []
    is_safe = True

    for category_result in data.get("categoriesAnalysis", []):
        category = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        if severity > 0:
            flagged_categories.append(category)
            is_safe = False
            details.append(
                {
                    "category": category,
                    "severity": severity,
                    "description": f"Content flagged for {category} with severity level {severity}",
                }
            )

    return UnsafeCopyCheckResponse(
        is_safe=is_safe,
        flagged_categories=flagged_categories,
        details=details,
    )


if __name__ == "__main__":
    req = UnsafeCopyCheckRequest(
        text="This is a safe localized message.",
        target_lang="fr",
    )
    resp = check_unsafe_copy(req)
    print(f"Safe: {resp.is_safe}")
    print(f"Flagged: {resp.flagged_categories}")
