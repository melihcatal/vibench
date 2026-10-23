import os
from typing import Optional, Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


class SafetyClient:
    """
    Local configuration and client helper for Azure AI Content Safety.
    """

    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        self.client = None

    def get_client(self) -> ContentSafetyClient:
        """Initialize and return the Azure Content Safety client."""
        if not self.endpoint or not self.key:
            raise ValueError("Azure Content Safety credentials not configured")

        if not self.client:
            self.client = ContentSafetyClient(
                self.endpoint, AzureKeyCredential(self.key)
            )
        return self.client

    def validate_credentials(self) -> bool:
        """Check if credentials are configured."""
        return bool(self.endpoint and self.key)


def load_config() -> Dict[str, Any]:
    """Load and return configuration for Azure AI Content Safety."""
    return {
        "endpoint": os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        "key": os.getenv("AZURE_CONTENT_SAFETY_KEY"),
        "default_categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "default_threshold": 4,
    }
