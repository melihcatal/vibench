import os
from typing import Dict, List, Any, Optional
import requests
from document_models import TextExtractionResponse


class OCRSafetyChecker:
    """Check extracted document text for unsafe content using Perspective API."""

    def __init__(self):
        self.api_key = os.environ.get("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

        self.api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def check_text_safety(
        self, text: str, attributes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze text for unsafe content using Perspective API.

        Args:
            text: Text to analyze
            attributes: List of attributes to check (TOXICITY, SEVERE_TOXICITY, IDENTITY_ATTACK, etc.)

        Returns:
            Dictionary with attribute scores and safety verdict
        """
        if attributes is None:
            attributes = [
                "TOXICITY",
                "SEVERE_TOXICITY",
                "IDENTITY_ATTACK",
                "INSULT",
                "PROFANITY",
                "THREAT",
            ]

        request_body = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {attr: {} for attr in attributes},
            "doNotStore": True,
        }

        params = {"key": self.api_key}

        response = requests.post(self.api_url, params=params, json=request_body)

        if response.status_code != 200:
            raise Exception(
                f"Perspective API error: {response.status_code} - {response.text}"
            )

        result = response.json()

        attribute_scores = {}
        for attr in attributes:
            if attr in result.get("attributeScores", {}):
                score = result["attributeScores"][attr]["summaryScore"]["value"]
                attribute_scores[attr] = score

        is_safe = all(score < 0.7 for score in attribute_scores.values())

        return {
            "attribute_scores": attribute_scores,
            "is_safe": is_safe,
            "raw_response": result,
            "provider": "perspective_api",
        }

    def check_extraction_safety(
        self,
        extraction_response: TextExtractionResponse,
        attributes: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Check safety of text from an OCR extraction response.
        """
        safety_result = self.check_text_safety(extraction_response.text, attributes)

        return {
            "extraction": extraction_response,
            "safety_check": safety_result,
            "overall_safe": safety_result["is_safe"],
        }

    def batch_check_safety(
        self, texts: List[str], attributes: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Check safety of multiple texts.
        """
        results = []
        for text in texts:
            result = self.check_text_safety(text, attributes)
            results.append(result)
        return results
