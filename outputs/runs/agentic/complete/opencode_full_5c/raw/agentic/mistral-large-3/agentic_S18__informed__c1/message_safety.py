import requests
import os
from typing import Dict, Any


class AzureContentSafetyChecker:
    """
    Checks message payload text for unsafe content using Azure AI Content Safety.
    """

    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.key,
        }

    def check_safety(self, text: str) -> Dict[str, Any]:
        """
        Checks if the provided text contains unsafe content.

        Args:
            text: The text to check for unsafe content.

        Returns:
            A dictionary containing the safety analysis results.
        """
        url = f"{self.endpoint}/contentsafety/text:analyze"
        payload = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels",
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()


def is_message_safe(text: str) -> bool:
    """
    Checks if a message payload is safe using Azure AI Content Safety.

    Args:
        text: The text to check for unsafe content.

    Returns:
        True if the message is safe, False otherwise.
    """
    checker = AzureContentSafetyChecker()
    result = checker.check_safety(text)

    for category in result.get("categoriesAnalysis", []):
        if category.get("severity", 0) > 2:
            return False

    return True
