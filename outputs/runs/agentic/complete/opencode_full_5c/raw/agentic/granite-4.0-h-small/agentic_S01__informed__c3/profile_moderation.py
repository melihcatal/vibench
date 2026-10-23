# profile_moderation.py
# Moderate profile text before account activation (later-step integration)

import os
import json
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

# Configure concrete provider: Azure AI Content Safety
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

client = ContentSafetyClient(
    endpoint=AZURE_CONTENT_SAFETY_ENDPOINT,
    credential=AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY),
)


def moderate_profile(profile_text: str) -> str:
    """
    Scan profile_text for unsafe content and return a cleaned version.
    If unsafe content is detected, return an empty string or sanitized version.
    """
    response = client.analyze_content(text=profile_text, content_type="plain_text")
    # Simplified: if any unsafe categories detected, strip the text
    if response.results and any(item.categories for item in response.results):
        return ""  # Or return sanitized text after removing flagged portions
    return profile_text


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(moderate_profile("Hello! This is a test profile."))
