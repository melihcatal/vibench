import os
import requests
import json
from typing import Dict, List, Any, Optional


def check_secret_labels_safety(
    labels: List[str], notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check secret labels and notes for unsafe text using Perspective API.

    Args:
        labels: List of secret labels/tags
        notes: Optional secret description or notes

    Returns:
        Safety analysis results
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    # Combine all text to check
    text_to_check = " ".join(labels)
    if notes:
        text_to_check += " " + notes

    if not text_to_check.strip():
        return {"safe": True, "message": "No text to check", "scores": {}}

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    # Request parameters for Perspective API
    params = {"key": api_key}

    # Request body
    data = {
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
        "doNotStore": True,
    }

    try:
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()

        result = response.json()

        # Extract scores
        attribute_scores = result.get("attributeScores", {})
        scores = {}

        for attribute, score_data in attribute_scores.items():
            summary_score = score_data.get("summaryScore", {})
            scores[attribute.lower()] = summary_score.get("value", 0)

        # Determine if safe (threshold: 0.7 for any attribute)
        max_score = max(scores.values()) if scores else 0
        is_safe = max_score < 0.7

        # Generate warnings for high scores
        warnings = []
        for attribute, score in scores.items():
            if score >= 0.7:
                warnings.append(f"High {attribute} score: {score:.2f}")

        return {
            "safe": is_safe,
            "text_checked": text_to_check,
            "scores": scores,
            "max_score": max_score,
            "warnings": warnings,
            "raw_response": result,
        }

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Perspective API request failed: {e}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse Perspective API response: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error checking text safety: {e}") from e


def analyze_secret_metadata_safety(secret_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze safety of secret metadata including name, description, and tags.

    Args:
        secret_metadata: Secret metadata dictionary

    Returns:
        Safety analysis with recommendations
    """
    # Extract text fields to check
    texts_to_check = []

    # Check secret name
    secret_name = secret_metadata.get("name", "")
    if secret_name:
        texts_to_check.append(f"Secret name: {secret_name}")

    # Check description
    description = secret_metadata.get("description", "")
    if description:
        texts_to_check.append(f"Description: {description}")

    # Check tags
    tags = secret_metadata.get("tags", {})
    if tags:
        tag_text = "Tags: " + ", ".join([f"{k}={v}" for k, v in tags.items()])
        texts_to_check.append(tag_text)

    # Combine all text
    combined_text = " ".join(texts_to_check)

    if not combined_text.strip():
        return {
            "safe": True,
            "message": "No metadata text to check",
            "recommendations": ["Add descriptive metadata to secrets"],
        }

    # Check safety using Perspective API
    safety_result = check_secret_labels_safety([combined_text])

    # Generate recommendations based on results
    recommendations = []

    if not safety_result["safe"]:
        recommendations.append("Review secret metadata for inappropriate content")

        warnings = safety_result.get("warnings", [])
        for warning in warnings:
            recommendations.append(f"Address: {warning}")

        # Specific recommendations based on attribute scores
        scores = safety_result.get("scores", {})

        if scores.get("toxicity", 0) > 0.5:
            recommendations.append("Avoid toxic language in secret descriptions")

        if scores.get("profanity", 0) > 0.5:
            recommendations.append("Remove profanity from secret metadata")

        if scores.get("threat", 0) > 0.5:
            recommendations.append("Remove threatening language from metadata")
    else:
        recommendations.append("Metadata appears safe and appropriate")

    # Add general best practices
    recommendations.append("Use clear, descriptive names without sensitive information")
    recommendations.append("Avoid including PII or sensitive data in descriptions")
    recommendations.append("Use tags for categorization, not for sensitive information")

    return {
        "safe": safety_result["safe"],
        "text_checked": combined_text,
        "scores": safety_result.get("scores", {}),
        "warnings": safety_result.get("warnings", []),
        "recommendations": recommendations,
        "metadata_fields_checked": len(texts_to_check),
    }


def validate_secret_name(name: str) -> Dict[str, Any]:
    """
    Validate a secret name for safety and best practices.

    Args:
        name: Secret name to validate

    Returns:
        Validation results
    """
    if not name or not name.strip():
        return {
            "valid": False,
            "errors": ["Secret name cannot be empty"],
            "warnings": [],
        }

    errors = []
    warnings = []

    # Check length
    if len(name) > 256:
        errors.append("Secret name exceeds 256 characters")
    elif len(name) > 128:
        warnings.append("Secret name is long (over 128 characters)")

    # Check for problematic patterns
    import re

    # Check for sensitive patterns
    sensitive_patterns = [
        r"password",
        r"secret",
        r"key",
        r"token",
        r"credential",
        r"admin",
        r"root",
        r"superuser",
        r"master",
    ]

    name_lower = name.lower()
    for pattern in sensitive_patterns:
        if re.search(pattern, name_lower):
            warnings.append(f"Name contains sensitive term: '{pattern}'")

    # Check for special characters (allow alphanumeric, hyphen, underscore, dot)
    if not re.match(r"^[a-zA-Z0-9_\-\./]+$", name):
        errors.append("Secret name contains invalid characters")

    # Check safety using Perspective API
    try:
        safety_result = check_secret_labels_safety([name])

        if not safety_result["safe"]:
            errors.append("Secret name contains unsafe content")
            warnings.extend(safety_result.get("warnings", []))
    except Exception as e:
        warnings.append(f"Could not complete safety check: {str(e)}")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "name": name,
        "length": len(name),
    }
