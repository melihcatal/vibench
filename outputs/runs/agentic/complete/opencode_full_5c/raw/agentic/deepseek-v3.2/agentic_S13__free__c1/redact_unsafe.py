import os
import re
from typing import Dict, Any, List, Tuple
from safety_client import SafetyClient


def redact_unsafe(text: str, redaction_char: str = "*") -> Dict[str, Any]:
    """
    Flags or redacts unsafe spans from text.

    Args:
        text: The text to analyze and redact
        redaction_char: Character to use for redaction

    Returns:
        Dictionary with redacted text and span information
    """
    client = SafetyClient.get_client()

    # Use Azure Content Safety API
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    # Create client
    safety_client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Analyze text
    request = AnalyzeTextOptions(text=text)
    response = safety_client.analyze_text(request)

    # Extract unsafe spans
    unsafe_spans = []
    redacted_text = text

    for category_result in response.categories_analysis:
        if category_result.severity > 0:
            # Get spans for this category
            spans = []
            for blocklist_result in response.blocklists_match or []:
                if blocklist_result.blocklist_name:
                    # Find and redact blocklist matches
                    for match in blocklist_result.blocklist_items or []:
                        if match.text:
                            # Redact the matched text
                            pattern = re.escape(match.text)
                            redacted_text = re.sub(
                                pattern, redaction_char * len(match.text), redacted_text
                            )
                            spans.append(
                                {
                                    "text": match.text,
                                    "start": text.find(match.text),
                                    "end": text.find(match.text) + len(match.text),
                                    "category": category_result.category.value,
                                    "severity": category_result.severity,
                                }
                            )

            unsafe_spans.extend(spans)

    # Sort spans by start position
    unsafe_spans.sort(key=lambda x: x["start"])

    return {
        "original_text": text,
        "redacted_text": redacted_text,
        "unsafe_spans": unsafe_spans,
        "redaction_char": redaction_char,
        "provider": "azure_content_safety",
        "model": "azure-content-safety-latest",
    }
