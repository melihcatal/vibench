import os
import json
from typing import Dict, Any, List
import requests


def check_text_safety(texts: List[str], language: str = "en") -> Dict[str, Any]:
    """
    Check user-generated document fields for unsafe content using Perspective API.

    Args:
        texts: List of text strings to check
        language: Language code for the text

    Returns:
        dict: Safety check results
    """
    try:
        # Perspective API configuration
        api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

        api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

        results = []

        for text in texts:
            # Prepare request for Perspective API
            request_data = {
                "comment": {"text": text, "type": "PLAIN_TEXT"},
                "languages": [language],
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

            # Call Perspective API
            response = requests.post(
                f"{api_url}?key={api_key}",
                json=request_data,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                result_data = response.json()

                # Extract attribute scores
                attribute_scores = {}
                for attr_name, attr_data in result_data.get(
                    "attributeScores", {}
                ).items():
                    score = attr_data.get("summaryScore", {}).get("value", 0)
                    attribute_scores[attr_name.lower()] = score

                # Determine overall safety
                max_score = max(attribute_scores.values()) if attribute_scores else 0
                is_safe = max_score < 0.7  # Threshold for safety

                results.append(
                    {
                        "text": text[:100] + "..." if len(text) > 100 else text,
                        "is_safe": is_safe,
                        "attribute_scores": attribute_scores,
                        "max_score": max_score,
                        "text_length": len(text),
                    }
                )
            else:
                results.append(
                    {
                        "text": text[:100] + "..." if len(text) > 100 else text,
                        "is_safe": None,
                        "error": f"API error: {response.status_code}",
                        "text_length": len(text),
                    }
                )

        # Calculate overall statistics
        safe_count = sum(1 for r in results if r.get("is_safe") is True)
        unsafe_count = sum(1 for r in results if r.get("is_safe") is False)
        error_count = sum(1 for r in results if r.get("is_safe") is None)

        return {
            "success": True,
            "results": results,
            "statistics": {
                "total_texts": len(texts),
                "safe_texts": safe_count,
                "unsafe_texts": unsafe_count,
                "error_texts": error_count,
                "safe_percentage": (safe_count / len(texts)) * 100 if texts else 0,
            },
            "provider": "Perspective API",
            "api_endpoint": "commentanalyzer.googleapis.com",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "total_texts": len(texts) if "texts" in locals() else 0,
            "provider": "Perspective API",
        }
