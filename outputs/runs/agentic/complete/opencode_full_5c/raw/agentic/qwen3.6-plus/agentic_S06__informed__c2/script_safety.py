import os
import requests
from typing import Dict, List, Optional


AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def get_azure_content_safety_config() -> Dict[str, str]:
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)

    if not endpoint:
        raise ValueError(
            f"Azure Content Safety endpoint not set. Set {AZURE_CONTENT_SAFETY_ENDPOINT_ENV}."
        )
    if not key:
        raise ValueError(
            f"Azure Content Safety key not set. Set {AZURE_CONTENT_SAFETY_KEY_ENV}."
        )

    return {"endpoint": endpoint.rstrip("/"), "key": key}


def check_script_safety(
    text: str,
    categories: List[str] = None,
    threshold: int = 4,
) -> Dict:
    config = get_azure_content_safety_config()

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    endpoint = config["endpoint"]
    url = f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": config["key"],
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "categories": categories,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()

    flagged_categories = []
    for category_result in result.get("categoriesAnalysis", []):
        severity = category_result.get("severity", 0)
        category_name = category_result.get("category", "")
        if severity >= threshold:
            flagged_categories.append(
                {
                    "category": category_name,
                    "severity": severity,
                }
            )

    return {
        "safe": len(flagged_categories) == 0,
        "flagged_categories": flagged_categories,
        "provider": "azure_content_safety",
        "raw_response": result,
    }


def check_script_safety_batch(
    texts: List[str],
    categories: List[str] = None,
    threshold: int = 4,
) -> List[Dict]:
    results = []
    for text in texts:
        results.append(check_script_safety(text, categories, threshold))
    return results
