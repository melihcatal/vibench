import os
import requests
from identity_models import ModerationResult


AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def moderate_profile_text(
    text: str,
    endpoint: str = None,
    api_key: str = None,
    output_type: str = "FourSeverityLevels",
) -> ModerationResult:
    endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required"
        )
    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    endpoint = endpoint.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    payload = {
        "text": text,
        "outputType": output_type,
    }

    response = requests.post(
        url, headers=headers, params=params, json=payload, timeout=30
    )
    response.raise_for_status()
    data = response.json()

    categories = {}
    flagged_text = []
    is_safe = True

    for category_result in data.get("categoriesAnalysis", []):
        category = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        categories[category] = severity
        if severity > 0:
            is_safe = False
            flagged_text.append(category)

    return ModerationResult(
        is_safe=is_safe,
        categories=categories,
        flagged_text=flagged_text,
        raw_response=data,
    )


def moderate_profile_fields(
    bio: str = "",
    display_name: str = "",
    location: str = "",
    endpoint: str = None,
    api_key: str = None,
) -> ModerationResult:
    combined_text = " ".join(filter(None, [bio, display_name, location]))
    if not combined_text.strip():
        return ModerationResult(is_safe=True, categories={}, flagged_text=[])
    return moderate_profile_text(combined_text, endpoint=endpoint, api_key=api_key)


if __name__ == "__main__":
    result = moderate_profile_text(
        text="Hello, I am a new user looking forward to connecting with others.",
    )
    print(result)
