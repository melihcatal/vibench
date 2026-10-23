import os
import json
import time
from typing import Dict, Any, List, Optional

import requests

from identity_models import UserProfile


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def moderate_claims_text(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    if not endpoint:
        endpoint = AZURE_CONTENT_SAFETY_ENDPOINT
    if not api_key:
        api_key = AZURE_CONTENT_SAFETY_KEY

    if not endpoint or not api_key:
        return {
            "success": False,
            "error": "missing_credentials",
            "message": "Azure Content Safety endpoint and API key are required",
            "provider": "azure_ai_content_safety",
        }

    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence",
        ],
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()

    result = response.json()

    flagged_categories = []
    for category_result in result.get("categoriesAnalysis", []):
        category = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        if severity > 0:
            flagged_categories.append(
                {
                    "category": category,
                    "severity": severity,
                }
            )

    is_flagged = len(flagged_categories) > 0

    return {
        "success": True,
        "is_flagged": is_flagged,
        "flagged_categories": flagged_categories,
        "blocklistsMatch": result.get("blocklistsMatch", []),
        "provider": "azure_ai_content_safety",
        "endpoint": endpoint,
        "analyzed_at": time.time(),
    }


def moderate_user_profile_notes(
    profile: Dict[str, Any],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    texts_to_check = []

    if profile.get("name"):
        texts_to_check.append({"field": "name", "text": profile["name"]})
    if profile.get("nickname"):
        texts_to_check.append({"field": "nickname", "text": profile["nickname"]})
    if profile.get("bio"):
        texts_to_check.append({"field": "bio", "text": profile["bio"]})
    if profile.get("notes"):
        texts_to_check.append({"field": "notes", "text": profile["notes"]})

    results = []
    overall_flagged = False

    for item in texts_to_check:
        moderation_result = moderate_claims_text(
            text=item["text"],
            endpoint=endpoint,
            api_key=api_key,
        )
        moderation_result["field"] = item["field"]
        results.append(moderation_result)
        if moderation_result.get("is_flagged"):
            overall_flagged = True

    return {
        "success": True,
        "overall_flagged": overall_flagged,
        "field_results": results,
        "provider": "azure_ai_content_safety",
        "analyzed_at": time.time(),
    }


def moderate_batch_claims(
    texts: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    results = []
    flagged_count = 0

    for text in texts:
        result = moderate_claims_text(text, endpoint, api_key)
        results.append(result)
        if result.get("is_flagged"):
            flagged_count += 1

    return {
        "success": True,
        "total_analyzed": len(texts),
        "flagged_count": flagged_count,
        "clean_count": len(texts) - flagged_count,
        "results": results,
        "provider": "azure_ai_content_safety",
        "analyzed_at": time.time(),
    }


if __name__ == "__main__":
    sample_text = "This is a test claim text for moderation purposes."
    result = moderate_claims_text(sample_text)
    print(json.dumps(result, indent=2))
