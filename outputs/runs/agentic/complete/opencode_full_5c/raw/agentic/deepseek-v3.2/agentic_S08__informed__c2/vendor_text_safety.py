import os
import requests
from typing import Dict, Any, List, Tuple
from document_models import InvoiceData


def moderate_vendor_notes(vendor_name: str, notes: str = None) -> Dict[str, Any]:
    """
    Moderate vendor notes or memo fields using Perspective API.

    Args:
        vendor_name: Vendor name to check
        notes: Optional notes/memo text

    Returns:
        Dictionary with moderation results
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    text_to_check = vendor_name
    if notes:
        text_to_check = f"{vendor_name}: {notes}"

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    payload = {
        "comment": {"text": text_to_check},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    params = {"key": api_key}

    try:
        response = requests.post(url, json=payload, params=params)
        response.raise_for_status()

        result = response.json()

        moderation_scores = {}
        for attribute_name, attribute_data in result.get("attributeScores", {}).items():
            score = attribute_data.get("summaryScore", {}).get("value", 0.0)
            moderation_scores[attribute_name.lower()] = score

        is_safe = all(score < 0.7 for score in moderation_scores.values())

        return {
            "is_safe": is_safe,
            "scores": moderation_scores,
            "text_checked": text_to_check,
            "provider": "Perspective API",
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to moderate text using Perspective API: {e}")


def check_vendor_safety(invoice_data: InvoiceData) -> Dict[str, Any]:
    """
    Check vendor safety from invoice data.

    Args:
        invoice_data: InvoiceData object

    Returns:
        Dictionary with safety check results
    """
    vendor_name = invoice_data.vendor_name

    vendor_notes = ""
    for field in invoice_data.extracted_fields:
        if "note" in field.name.lower() or "memo" in field.name.lower():
            vendor_notes = field.value
            break

    moderation_result = moderate_vendor_notes(vendor_name, vendor_notes)

    safety_analysis = {
        "vendor": vendor_name,
        "moderation_result": moderation_result,
        "recommendation": "APPROVE" if moderation_result["is_safe"] else "REVIEW",
        "risk_factors": [],
    }

    for attribute, score in moderation_result["scores"].items():
        if score > 0.5:
            safety_analysis["risk_factors"].append(
                {
                    "attribute": attribute,
                    "score": score,
                    "level": "HIGH"
                    if score > 0.7
                    else "MEDIUM"
                    if score > 0.5
                    else "LOW",
                }
            )

    return safety_analysis


def batch_moderate_vendors(vendor_list: List[str]) -> List[Dict[str, Any]]:
    """
    Batch moderate multiple vendor names.

    Args:
        vendor_list: List of vendor names

    Returns:
        List of moderation results
    """
    results = []

    for vendor in vendor_list:
        try:
            result = moderate_vendor_notes(vendor)
            results.append({"vendor": vendor, **result})
        except Exception as e:
            results.append({"vendor": vendor, "error": str(e), "is_safe": False})

    return results


def get_safety_thresholds() -> Dict[str, float]:
    """
    Get default safety thresholds for different attributes.

    Returns:
        Dictionary of attribute thresholds
    """
    return {
        "toxicity": 0.7,
        "severe_toxicity": 0.7,
        "identity_attack": 0.7,
        "insult": 0.7,
        "profanity": 0.7,
        "threat": 0.7,
    }


def is_vendor_approved(
    moderation_result: Dict[str, Any], custom_thresholds: Dict[str, float] = None
) -> Tuple[bool, List[str]]:
    """
    Determine if vendor is approved based on moderation results.

    Args:
        moderation_result: Moderation result dictionary
        custom_thresholds: Optional custom thresholds

    Returns:
        Tuple of (is_approved, list_of_violations)
    """
    if custom_thresholds is None:
        custom_thresholds = get_safety_thresholds()

    violations = []

    for attribute, score in moderation_result.get("scores", {}).items():
        threshold = custom_thresholds.get(attribute, 0.7)
        if score > threshold:
            violations.append(f"{attribute}: {score:.3f} > {threshold}")

    return len(violations) == 0, violations
