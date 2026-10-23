import os
import json
from typing import Dict, Any, List
import requests


def check_text_safety(text: str, categories: List[str] = None) -> Dict[str, Any]:
    """
    Check user-generated text for unsafe content using Perspective API.

    Args:
        text: Text to check for safety
        categories: List of toxicity categories to check

    Returns:
        dict: Safety check result
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")

    if not api_key:
        return {
            "success": False,
            "error": "PERSPECTIVE_API_KEY environment variable is not set",
            "safe": False,
        }

    if not text or not text.strip():
        return {
            "success": True,
            "safe": True,
            "message": "Empty text is considered safe",
        }

    # Default categories if not specified
    if not categories:
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
    }

    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()

        result = response.json()

        # Extract scores
        scores = {}
        for category in categories:
            if category in result.get("attributeScores", {}):
                score = result["attributeScores"][category]["summaryScore"]["value"]
                scores[category] = score

        # Determine if text is safe (threshold: 0.7 for any category)
        max_score = max(scores.values()) if scores else 0
        is_safe = max_score < 0.7

        return {
            "success": True,
            "safe": is_safe,
            "scores": scores,
            "max_score": max_score,
            "text_length": len(text),
            "provider": "Perspective API",
        }
    except Exception as e:
        return {"success": False, "error": str(e), "safe": False}


def check_document_safety(
    document: Dict[str, Any], text_fields: List[str] = None
) -> Dict[str, Any]:
    """
    Check user-generated document fields for unsafe content.

    Args:
        document: Document to check
        text_fields: List of field names containing text to check

    Returns:
        dict: Safety check result for the document
    """
    if not text_fields:
        # Default text fields to check
        text_fields = ["content", "description", "title", "comment", "feedback"]

    results = {}
    unsafe_fields = []

    for field in text_fields:
        if field in document and isinstance(document[field], str):
            text = document[field]
            if text.strip():  # Only check non-empty text
                safety_result = check_text_safety(text)
                results[field] = safety_result

                if not safety_result.get("safe", False):
                    unsafe_fields.append(field)

    # Overall document safety
    is_safe = len(unsafe_fields) == 0

    return {
        "success": True,
        "document_safe": is_safe,
        "unsafe_fields": unsafe_fields,
        "field_results": results,
        "document_id": document.get("_id", "unknown"),
        "provider": "Perspective API",
    }


def check_batch_safety(
    documents: List[Dict[str, Any]], text_field: str = "content"
) -> Dict[str, Any]:
    """
    Check multiple documents for safety in batch.

    Args:
        documents: List of documents to check
        text_field: Field name containing text to check

    Returns:
        dict: Batch safety check results
    """
    safe_docs = []
    unsafe_docs = []

    for doc in documents:
        if text_field in doc and isinstance(doc[text_field], str):
            safety_result = check_text_safety(doc[text_field])

            if safety_result.get("success", False) and safety_result.get("safe", False):
                safe_docs.append(
                    {
                        "document_id": doc.get("_id", "unknown"),
                        "safety_score": safety_result.get("max_score", 0),
                    }
                )
            else:
                unsafe_docs.append(
                    {
                        "document_id": doc.get("_id", "unknown"),
                        "safety_score": safety_result.get("max_score", 1.0),
                        "error": safety_result.get("error"),
                    }
                )

    return {
        "success": True,
        "total_documents": len(documents),
        "safe_documents": len(safe_docs),
        "unsafe_documents": len(unsafe_docs),
        "safe_docs": safe_docs,
        "unsafe_docs": unsafe_docs,
        "provider": "Perspective API",
    }
