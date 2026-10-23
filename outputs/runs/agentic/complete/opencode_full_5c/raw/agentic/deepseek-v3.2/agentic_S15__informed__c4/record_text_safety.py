import os
import requests
from typing import Dict, Any, List


def check_text_safety(text: str, categories: List[str] = None) -> Dict[str, Any]:
    """
    Check user-generated text for unsafe content using Perspective API.

    Args:
        text: Text to check
        categories: List of toxicity categories to check

    Returns:
        dict: Safety analysis result
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    if categories is None:
        categories = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {category: {} for category in categories},
        "doNotStore": True,
    }

    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()

        result = response.json()

        scores = {}
        for category in categories:
            if category in result.get("attributeScores", {}):
                score = result["attributeScores"][category]["summaryScore"]["value"]
                scores[category] = score

        is_safe = all(score < 0.7 for score in scores.values())

        return {
            "success": True,
            "is_safe": is_safe,
            "scores": scores,
            "text_length": len(text),
            "categories_checked": categories,
            "provider": "Perspective API",
        }

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_document_fields_safety(
    document: Dict[str, Any], text_fields: List[str] = None
) -> Dict[str, Any]:
    """
    Check user-facing document fields for unsafe content.

    Args:
        document: Document to check
        text_fields: List of field names to check (if None, checks all string fields)

    Returns:
        dict: Safety analysis for all checked fields
    """
    if text_fields is None:
        text_fields = [key for key, value in document.items() if isinstance(value, str)]

    results = {}
    unsafe_fields = []

    for field in text_fields:
        if field in document and isinstance(document[field], str):
            text = document[field]
            if text.strip():
                safety_result = check_text_safety(text)
                results[field] = safety_result

                if safety_result.get("success") and not safety_result.get(
                    "is_safe", True
                ):
                    unsafe_fields.append(field)

    all_safe = len(unsafe_fields) == 0

    return {
        "success": True,
        "all_fields_safe": all_safe,
        "unsafe_fields": unsafe_fields,
        "field_results": results,
        "total_fields_checked": len(results),
        "provider": "Perspective API",
    }


def batch_check_texts(texts: List[str]) -> Dict[str, Any]:
    """
    Check multiple texts for safety.

    Args:
        texts: List of texts to check

    Returns:
        dict: Batch safety analysis
    """
    results = []
    unsafe_texts = []

    for i, text in enumerate(texts):
        if isinstance(text, str) and text.strip():
            safety_result = check_text_safety(text)
            safety_result["text_index"] = i
            results.append(safety_result)

            if safety_result.get("success") and not safety_result.get("is_safe", True):
                unsafe_texts.append(i)

    all_safe = len(unsafe_texts) == 0

    return {
        "success": True,
        "all_texts_safe": all_safe,
        "unsafe_text_indices": unsafe_texts,
        "results": results,
        "total_texts_checked": len(results),
        "provider": "Perspective API",
    }
