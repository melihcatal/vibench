"""
Check narration scripts for unsafe content using Azure AI Content Safety.

This module provides content moderation for narration scripts before
synthesis, checking for hate speech, violence, self-harm, and sexual
content using Azure AI Content Safety service.

Provider: Azure AI Content Safety (api.content-safety.azure.com)
API Version: 2024-02-15-preview
"""

import os
from typing import Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

# Azure Content Safety configuration
CONTENT_SAFETY_ENDPOINT = os.getenv(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/"
)
CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")

# Severity thresholds (0-4 scale used by Azure Content Safety)
DEFAULT_THRESHOLD = 2  # Medium severity triggers flag


def get_content_safety_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ContentSafetyClient:
    """
    Create an Azure AI Content Safety client.
    
    Args:
        endpoint: Azure Content Safety endpoint URL
        api_key: Azure API key
        
    Returns:
        Configured ContentSafetyClient
    """
    ep = endpoint or CONTENT_SAFETY_ENDPOINT
    key = api_key or CONTENT_SAFETY_KEY
    
    credential = AzureKeyCredential(key)
    return ContentSafetyClient(endpoint=ep, credential=credential)


def check_script_safety(
    text: str,
    threshold: int = DEFAULT_THRESHOLD,
    client: Optional[ContentSafetyClient] = None,
) -> dict:
    """
    Check narration script for unsafe content using Azure Content Safety.
    
    Analyzes text for Hate, SelfHarm, Sexual, and Violence categories.
    
    Args:
        text: Narration script text to analyze
        threshold: Severity level to flag (0-4, where 4 is most severe)
        client: Optional pre-configured ContentSafetyClient
        
    Returns:
        Dict with safety analysis results
    """
    if not client:
        client = get_content_safety_client()
    
    request = AnalyzeTextOptions(text=text)
    
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {
            "safe": False,
            "error": str(e),
            "categories": {},
        }
    
    categories = {}
    is_safe = True
    
    for category_result in response.categories_analysis:
        category_name = category_result.category
        severity = category_result.severity or 0
        flagged = severity >= threshold
        
        categories[category_name] = {
            "severity": severity,
            "flagged": flagged,
        }
        
        if flagged:
            is_safe = False
    
    return {
        "safe": is_safe,
        "threshold": threshold,
        "categories": categories,
        "blocklists_matched": response.blocklists_result.blocklist_name if hasattr(response, 'blocklists_result') and response.blocklists_result else [],
    }


def get_safety_categories() -> list[str]:
    """
    Get list of content safety categories from Azure Content Safety.
    
    Returns:
        List of category names (Hate, SelfHarm, Sexual, Violence)
    """
    return [
        TextCategory.HATE.value,
        TextCategory.SELF_HARM.value,
        TextCategory.SEXUAL.value,
        TextCategory.VIOLENCE.value,
    ]


def check_script_safe_bool(
    text: str,
    threshold: int = DEFAULT_THRESHOLD,
    client: Optional[ContentSafetyClient] = None,
) -> bool:
    """
    Quick boolean check if script is safe for synthesis.
    
    Args:
        text: Text to check
        threshold: Severity threshold for flagging
        client: Optional ContentSafetyClient
        
    Returns:
        True if text is safe, False if any category exceeds threshold
    """
    result = check_script_safety(text, threshold=threshold, client=client)
    return result.get("safe", False)


if __name__ == "__main__":
    sample_safe = "Hello, welcome to our friendly narration service."
    sample_unsafe = "I hate everyone and want to cause harm."
    
    print("Checking safe text:")
    result = check_script_safety(sample_safe)
    print(f"Safe: {result['safe']}, Categories: {result['categories']}")
    
    print("\nChecking unsafe text:")
    result = check_script_safety(sample_unsafe)
    print(f"Safe: {result['safe']}, Categories: {result['categories']}")
