import os
import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"
AZURE_CONTENT_SAFETY_ANALYZE_URL = (
    f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze"
    f"?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
)

DEFAULT_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]


def moderate_profile_text(text: str, categories: list = None) -> dict:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set"
        )

    categories = categories or DEFAULT_CATEGORIES

    payload = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
    }

    resp = requests.post(
        AZURE_CONTENT_SAFETY_ANALYZE_URL,
        json=payload,
        headers=headers,
        timeout=30,
    )

    if resp.status_code != 200:
        raise RuntimeError(
            f"Azure AI Content Safety moderation failed with status {resp.status_code}: {resp.text}"
        )

    result = resp.json()
    return _parse_moderation_result(result)


def _parse_moderation_result(result: dict) -> dict:
    categories_result = result.get("categoriesAnalysis", [])
    blocklist_matches = result.get("blocklistsMatch", [])

    highest_severity = 0
    flagged_categories = []

    for cat_analysis in categories_result:
        severity = cat_analysis.get("severity", 0)
        category = cat_analysis.get("category", "")
        if severity > highest_severity:
            highest_severity = severity
        if severity > 0:
            flagged_categories.append(
                {
                    "category": category,
                    "severity": severity,
                }
            )

    is_safe = highest_severity <= 2 and not blocklist_matches

    return {
        "is_safe": is_safe,
        "highest_severity": highest_severity,
        "flagged_categories": flagged_categories,
        "blocklist_matches": blocklist_matches,
        "raw_result": result,
    }


def is_profile_approved(text: str, max_severity: int = 2) -> bool:
    result = moderate_profile_text(text)
    return result["is_safe"] and result["highest_severity"] <= max_severity


if __name__ == "__main__":
    import sys

    text = sys.argv[1] if len(sys.argv) > 1 else "Hello, this is my profile bio."
    result = moderate_profile_text(text)
    print(f"Profile safe: {result['is_safe']}")
    print(f"Highest severity: {result['highest_severity']}")
