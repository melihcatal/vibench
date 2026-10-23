import os
import re
from typing import List

# Azure Content Safety SDK import (concrete provider signal)
from azure.ai.contentsafety import ContentSafetyClient

# Environment variables for authentication
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
    raise RuntimeError("Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars")

CONTENT_SAFETY_CLIENT = ContentSafetyClient(
    endpoint=AZURE_CONTENT_SAFETY_ENDPOINT, credential=AZURE_CONTENT_SAFETY_KEY
)

def check_script_for_unsafe_content(script: str) -> List[dict]:
    """Send a narration script to Azure Content Safety and return moderation results.

    Args:
        script: The raw narration text or SSML.

    Returns:
        List of moderation result dicts containing fields like 'category', 'severity', 'detail'.
    """
    response = CONTENT_SAFETY_CLIENT.analyze_content(text=script)
    # The SDK returns a list of moderation categories; flatten to simple list
    results = [
        {
            "category": item.category,
            "severity": item.severity,
            "detail": item.detail,
        }
        for item in response.results
    ]
    return results

if __name__ == "__main__":
    demo_script = "Hey there! This is a test. Mentioning violence is not okay."
    safety = check_script_for_unsafe_content(demo_script)
    if safety:
        print("Unsafe content detected:")
        for issue in safety:
            print(issue)
    else:
        print("Script passed safety check.")
