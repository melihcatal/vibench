import os
import json
from typing import Dict, Any, List, Optional
import requests


def check_text_safety(text: str, language: str = "en") -> Dict[str, Any]:
    """
    Check user-generated text for unsafe content using Perspective API.

    Args:
        text: Text to check for safety
        language: Language code for the text

    Returns:
        dict: Safety analysis results
    """
    try:
        # Perspective API key from environment variable
        api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

        # Perspective API endpoint
        url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

        # Prepare request payload
        payload = {
            "comment": {"text": text, "type": "PLAIN_TEXT"},
            "languages": [language],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
                "SEXUALLY_EXPLICIT": {},
                "FLIRTATION": {},
            },
            "doNotStore": True,
        }

        # Make API request
        params = {"key": api_key}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()

        result = response.json()

        # Extract attribute scores
        attribute_scores = result.get("attributeScores", {})

        # Calculate overall safety score (average of all attributes)
        scores = []
        safety_summary = {}

        for attr_name, attr_data in attribute_scores.items():
            score = attr_data.get("summaryScore", {}).get("value", 0)
            scores.append(score)
            safety_summary[attr_name.lower()] = {
                "score": score,
                "threshold_exceeded": score > 0.7,  # Common threshold for moderation
            }

        overall_score = sum(scores) / len(scores) if scores else 0

        # Determine safety status
        if overall_score > 0.8:
            safety_status = "UNSAFE"
        elif overall_score > 0.5:
            safety_status = "SUSPICIOUS"
        else:
            safety_status = "SAFE"

        return {
            "success": True,
            "safety_status": safety_status,
            "overall_score": overall_score,
            "attribute_scores": safety_summary,
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "provider": "Perspective API",
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Perspective API request failed: {str(e)}",
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
        }


def check_document_fields_safety(
    document: Dict[str, Any], fields_to_check: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Check specific fields in a document for unsafe content.

    Args:
        document: Document containing fields to check
        fields_to_check: List of field names to check (if None, checks all string fields)

    Returns:
        dict: Safety analysis for all checked fields
    """
    try:
        if fields_to_check is None:
            # Check all string fields that don't start with underscore
            fields_to_check = [
                key
                for key, value in document.items()
                if not key.startswith("_") and isinstance(value, str)
            ]

        field_results = {}
        unsafe_fields = []

        for field_name in fields_to_check:
            if field_name in document and isinstance(document[field_name], str):
                text = document[field_name]
                if text.strip():  # Only check non-empty strings
                    safety_result = check_text_safety(text)

                    field_results[field_name] = {
                        "safety_status": safety_result.get("safety_status"),
                        "overall_score": safety_result.get("overall_score"),
                        "text_preview": text[:50] + "..." if len(text) > 50 else text,
                    }

                    if safety_result.get("safety_status") in ["UNSAFE", "SUSPICIOUS"]:
                        unsafe_fields.append(field_name)

        # Determine overall document safety
        if unsafe_fields:
            if any(
                field_results[f]["safety_status"] == "UNSAFE" for f in unsafe_fields
            ):
                doc_safety_status = "UNSAFE"
            else:
                doc_safety_status = "SUSPICIOUS"
        else:
            doc_safety_status = "SAFE"

        return {
            "success": True,
            "document_safety_status": doc_safety_status,
            "field_results": field_results,
            "unsafe_fields": unsafe_fields,
            "document_id": document.get("_id", "unknown"),
            "fields_checked": fields_to_check,
            "provider": "Perspective API",
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error checking document safety: {str(e)}",
            "document_id": document.get("_id", "unknown"),
        }


def batch_check_texts(texts: List[str], language: str = "en") -> Dict[str, Any]:
    """
    Check multiple texts for safety in batch.

    Args:
        texts: List of texts to check
        language: Language code for the texts

    Returns:
        dict: Batch safety analysis results
    """
    results = []
    unsafe_count = 0
    suspicious_count = 0

    for i, text in enumerate(texts):
        safety_result = check_text_safety(text, language)

        result_entry = {
            "text_index": i,
            "text_preview": text[:50] + "..." if len(text) > 50 else text,
            "safety_status": safety_result.get("safety_status"),
            "overall_score": safety_result.get("overall_score"),
        }

        if safety_result.get("safety_status") == "UNSAFE":
            unsafe_count += 1
        elif safety_result.get("safety_status") == "SUSPICIOUS":
            suspicious_count += 1

        results.append(result_entry)

    return {
        "success": True,
        "total_texts": len(texts),
        "unsafe_count": unsafe_count,
        "suspicious_count": suspicious_count,
        "safe_count": len(texts) - unsafe_count - suspicious_count,
        "results": results,
        "provider": "Perspective API",
    }
