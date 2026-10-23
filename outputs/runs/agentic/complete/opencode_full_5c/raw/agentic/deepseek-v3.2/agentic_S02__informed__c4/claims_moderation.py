import os
import requests
import json
from typing import Dict, Any, List


def moderate_user_claims(user_claims: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")

    if not api_key or not endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_KEY and AZURE_CONTENT_SAFETY_ENDPOINT environment variables are required"
        )

    text_to_moderate = ""

    if "name" in user_claims and user_claims["name"]:
        text_to_moderate += f"Name: {user_claims['name']}\n"
    if "nickname" in user_claims and user_claims["nickname"]:
        text_to_moderate += f"Nickname: {user_claims['nickname']}\n"

    if not text_to_moderate.strip():
        return {
            "moderation_result": "no_text_to_moderate",
            "safe": True,
            "provider": "azure_content_safety",
            "original_claims": user_claims,
        }

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}

    payload = {
        "text": text_to_moderate,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        categories_analysis = result.get("categoriesAnalysis", [])

        has_violations = False
        violations = []

        for category in categories_analysis:
            if category.get("severity", 0) > 0:
                has_violations = True
                violations.append(
                    {
                        "category": category.get("category"),
                        "severity": category.get("severity"),
                        "severity_level": _get_severity_level(
                            category.get("severity", 0)
                        ),
                    }
                )

        moderation_result = {
            "moderation_result": "violations_found" if has_violations else "safe",
            "safe": not has_violations,
            "violations": violations,
            "text_analyzed": text_to_moderate,
            "provider": "azure_content_safety",
            "endpoint_used": endpoint,
            "original_claims": user_claims,
        }

        return moderation_result

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Failed to moderate claims with Azure Content Safety: {str(e)}"
        )


def _get_severity_level(severity: int) -> str:
    if severity == 0:
        return "Safe"
    elif severity == 2:
        return "Low"
    elif severity == 4:
        return "Medium"
    elif severity == 6:
        return "High"
    else:
        return "Unknown"


def batch_moderate_claims(claims_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []

    for claims in claims_list:
        try:
            moderation_result = moderate_user_claims(claims)
            results.append(
                {
                    "user_id": claims.get("user_id", "unknown"),
                    "moderation_result": moderation_result,
                }
            )
        except Exception as e:
            results.append(
                {
                    "user_id": claims.get("user_id", "unknown"),
                    "moderation_result": {
                        "error": str(e),
                        "safe": False,
                        "provider": "azure_content_safety",
                    },
                }
            )

    return results


if __name__ == "__main__":
    sample_claims = {
        "user_id": "user123",
        "name": "John Doe",
        "nickname": "Johnny",
        "email": "john@example.com",
    }

    result = moderate_user_claims(sample_claims)
    print(f"Moderation result: {result['moderation_result']}")
    print(f"Safe: {result['safe']}")
    if result["violations"]:
        print(f"Violations: {result['violations']}")
