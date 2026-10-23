import os
from typing import List, Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import SafetyClient

def redact_unsafe(text_content: str, blocklist_names: List[str] = None) -> Dict[str, Any]:
    """
    Flags or redacts unsafe spans from text using Azure Content Safety blocklist functionality.
    Note: Azure Content Safety's direct redaction is not exposed via SDK for categories.
    This function will use blocklist to identify and flag content.
    """
    safety_client = SafetyClient()
    client = safety_client.get_client()

    if blocklist_names is None:
        blocklist_names = [] # Use an empty list if no blocklist is provided

    request = AnalyzeTextOptions(text=text_content, blocklist_names=blocklist_names)

    try:
        response = client.analyze_text(request)
        # For demonstration, we'll just indicate if blocklist matches were found
        # In a real scenario, you'd integrate with blocklist management to get flagged terms
        # and perform redaction client-side if the service doesn't provide it directly.
        flagged_spans = []
        if response.blocklist_matches:
            for match in response.blocklist_matches:
                flagged_spans.append({
                    "blocklist_name": match.blocklist_name,
                    "block_item_text": match.block_item_text,
                    "start_index": match.offset,
                    "length": match.length
                })
        
        # This is a simplified representation. Actual redaction logic would replace the flagged spans.
        redaction_status = "No unsafe content to redact" 
        if flagged_spans:
            redaction_status = "Content flagged by blocklist. Manual redaction may be needed."

        return {
            "original_text": text_content,
            "flagged_spans": flagged_spans,
            "redaction_status": redaction_status
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example Usage: You need to have blocklists configured in your Azure Content Safety resource
    # and provide their names here. For this example, we'll assume a blocklist named 'test_blocklist'
    # contains terms like 'badword'.
    test_text_with_unsafe = "This is a badword and another badword here."
    # To run this example, ensure 'test_blocklist' exists in your Azure Content Safety resource
    # with relevant terms.
    results = redact_unsafe(test_text_with_unsafe, blocklist_names=["test_blocklist"])
    print(f"Redaction results for '{test_text_with_unsafe}': {results}")

    test_text_clean = "This is a clean sentence."
    results_clean = redact_unsafe(test_text_clean, blocklist_names=["test_blocklist"])
    print(f"Redaction results for '{test_text_clean}': {results_clean}")
