"""
claims_moderation.py - Moderate free-text claims or notes from federated
login profiles using content safety analysis.

Provider: Azure AI Content Safety
SDK: requests (REST API)
Auth env vars: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
from typing import Optional

import requests


AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def get_azure_content_safety_config() -> tuple[str, str]:
    """
    Retrieve Azure AI Content Safety configuration from environment variables.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

    if not endpoint or not api_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "environment variables must be set"
        )

    # Normalize endpoint: remove trailing slash
    endpoint = endpoint.rstrip("/")
    return endpoint, api_key


def moderate_text(
    text: str,
    categories: Optional[list[str]] = None,
    output_type: str = "EightSeverityLevels",
) -> dict:
    """
    Send text to Azure AI Content Safety for moderation analysis.

    Categories: Hate, SelfHarm, Sexual, Violence
    Output types: FourSeverityLevels or EightSeverityLevels

    Returns the moderation result with category scores.
    """
    endpoint, api_key = get_azure_content_safety_config()

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    url = f"{endpoint}/contentsafety/text:analyze"

    params = {
        "api-version": AZURE_CONTENT_SAFETY_API_VERSION,
    }

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "categories": categories,
        "outputType": output_type,
    }

    response = requests.post(url, params=params, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()


def moderate_user_claims(
    user_claims: dict,
    text_fields: Optional[list[str]] = None,
) -> dict:
    """
    Moderate free-text fields in federated user claims using
    Azure AI Content Safety.

    Checks fields like display_name, given_name, surname, and any
    custom profile notes for inappropriate content.

    Returns a dict with moderation results per field and an overall
    moderation status.
    """
    if text_fields is None:
        text_fields = ["display_name", "given_name", "surname", "notes", "bio"]

    results = {}
    flagged = False

    for field_name in text_fields:
        value = user_claims.get(field_name, "")
        if not value or not isinstance(value, str):
            continue

        try:
            moderation_result = moderate_text(value)
            category_results = moderation_result.get("categoriesAnalysis", [])

            field_flagged = False
            for cat_result in category_results:
                severity = cat_result.get("severity", 0)
                if severity > 0:
                    field_flagged = True
                    flagged = True

            results[field_name] = {
                "flagged": field_flagged,
                "categories": category_results,
                "original_value": value if not field_flagged else "[REDACTED]",
            }
        except requests.RequestException as e:
            results[field_name] = {
                "flagged": False,
                "error": str(e),
                "original_value": value,
            }

    return {
        "provider": "azure_content_safety",
        "overall_flagged": flagged,
        "field_results": results,
        "moderated_fields": list(results.keys()),
    }


def batch_moderate_texts(
    texts: list[str],
    categories: Optional[list[str]] = None,
) -> list[dict]:
    """
    Moderate multiple text strings using Azure AI Content Safety
    text analysis API.

    Returns a list of moderation results corresponding to each input text.
    """
    endpoint, api_key = get_azure_content_safety_config()

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    url = f"{endpoint}/contentsafety/text:analyze"

    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    results = []
    for text in texts:
        payload = {
            "text": text,
            "categories": categories,
            "outputType": "EightSeverityLevels",
        }

        response = requests.post(url, params=params, headers=headers, json=payload)
        response.raise_for_status()
        results.append(response.json())

    return results
