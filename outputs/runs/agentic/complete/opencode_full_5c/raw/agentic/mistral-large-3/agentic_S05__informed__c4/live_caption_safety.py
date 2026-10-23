import os
import requests
from typing import AsyncGenerator


class LiveCaptionSafetyChecker:
    """Check live transcript text for unsafe content using Azure AI Content Safety."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.key:
            raise ValueError("Azure Content Safety credentials not set")

    async def check_safety(
        self, captions: AsyncGenerator[str, None]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Check live captions for unsafe content."""
        url = f"{self.endpoint}/contentsafety/text:analyze"
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }

        async for caption in captions:
            payload = {
                "text": caption,
                "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            yield response.json()
