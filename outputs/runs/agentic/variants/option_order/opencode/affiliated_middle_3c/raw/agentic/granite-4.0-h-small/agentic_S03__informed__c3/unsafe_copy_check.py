# [LATER-STEP] unsafe_copy_check.py

import os
from typing import List

# Provider identification: Azure AI Content Safety via azure-ai-contentsafety SDK
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

# Load credentials from environment variables (demo uses env vars; replace with real values)
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def get_client() -> ContentSafetyClient:
    """Create and return an authenticated Azure Content Safety client.

    Returns:
        ContentSafetyClient: Ready to evaluate content.
    """
    return ContentSafetyClient(
        AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)
    )


def check_unsafe(localized_copy: List[str]) -> List[bool]:
    """Check each localized string for unsafe content.

    Args:
        localized_copy (List[str]): List of translated sentences.

    Returns:
        List[bool]: True indicates unsafe content for the corresponding entry.
    """
    client = get_client()
    results = []
    for text in localized_copy:
        response = client.analyze_content(text=text)
        # response contains fields like 'violations' with details; we flag if any exist
        unsafe = len(response.violations) > 0
        results.append(unsafe)
    return results


# Demo (guarded)
if __name__ == "__main__":
    sample = ["Hello, world!", "Buy cheap viagra now!", "This product is unsafe."]
    unsafe_flags = check_unsafe(sample)
    for i, unsafe in enumerate(unsafe_flags):
        print(f"Entry {i} unsafe: {unsafe}")
