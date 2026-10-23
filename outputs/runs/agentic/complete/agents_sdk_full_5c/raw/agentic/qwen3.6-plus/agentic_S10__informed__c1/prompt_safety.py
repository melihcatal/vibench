"""
Check prompts and generated text for unsafe content using Azure AI Content Safety.
Provider: Azure AI Content Safety API
SDK: requests (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
import requests
from typing import Dict, Any, List, Optional


# Provider-specific environment variables
AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

# Azure AI Content Safety API version
API_VERSION = "2024-02-15-preview"


class AzureContentSafetyChecker:
    """Client for Azure AI Content Safety text analysis."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.endpoint = (endpoint or AZURE_CONTENT_SAFETY_ENDPOINT).rstrip("/")
        self.api_key = api_key or AZURE_CONTENT_SAFETY_KEY
        self.api_version = API_VERSION

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _build_url(self, path: str) -> str:
        return f"{self.endpoint}/{path}?api-version={self.api_version}"

    def analyze_text(
        self,
        text: str,
        categories: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze text for unsafe content categories.

        Args:
            text: The text to analyze.
            categories: Optional list of categories to check.
                        Defaults to ["Hate", "SelfHarm", "Sexual", "Violence"].

        Returns:
            Dictionary with analysis results including severity levels.
        """
        if categories is None:
            categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

        payload = {
            "text": text,
            "categories": categories,
            "outputType": "EightSeverityLevels",
        }

        url = self._build_url("text:analyze")
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def is_text_safe(
        self,
        text: str,
        max_severity: int = 2,
    ) -> Dict[str, Any]:
        """
        Check if text is safe based on severity thresholds.

        Args:
            text: The text to check.
            max_severity: Maximum allowed severity level (0-7).

        Returns:
            Dictionary with safe flag and category details.
        """
        result = self.analyze_text(text)
        category_results = result.get("categoriesAnalysis", [])

        unsafe_categories = []
        for cat in category_results:
            severity = cat.get("severity", 0)
            if severity > max_severity:
                unsafe_categories.append({
                    "category": cat.get("category", ""),
                    "severity": severity,
                })

        return {
            "is_safe": len(unsafe_categories) == 0,
            "unsafe_categories": unsafe_categories,
            "full_result": result,
        }

    def analyze_prompt_and_response(
        self,
        prompt: str,
        response_text: str,
    ) -> Dict[str, Any]:
        """
        Analyze both a user prompt and a generated response for safety.

        Args:
            prompt: The user prompt to check.
            response_text: The model-generated response to check.

        Returns:
            Dictionary with safety analysis for both prompt and response.
        """
        prompt_safety = self.is_text_safe(prompt)
        response_safety = self.is_text_safe(response_text)

        return {
            "prompt_safe": prompt_safety["is_safe"],
            "prompt_details": prompt_safety,
            "response_safe": response_safety["is_safe"],
            "response_details": response_safety,
            "overall_safe": prompt_safety["is_safe"] and response_safety["is_safe"],
        }


def check_prompt_safety(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Quick function to check if text is safe.

    Args:
        text: The text to analyze.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Returns:
        Safety analysis result.
    """
    checker = AzureContentSafetyChecker(endpoint=endpoint, api_key=api_key)
    return checker.is_text_safe(text)


if __name__ == "__main__":
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        print("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required.")
    else:
        checker = AzureContentSafetyChecker()
        test_text = "This is a perfectly safe and friendly message."
        result = checker.is_text_safe(test_text)
        print(f"Text safety check: {result}")
