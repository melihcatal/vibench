"""Flags or redacts unsafe spans from text using Azure AI Content Safety."""
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextBlocklist
from safety_client import get_azure_content_safety_client
from safety_models import RedactionResult


def redact_unsafe_azure(text_to_redact: str) -> RedactionResult:
    """
    Analyzes text and redacts content from custom blocklists using Azure.

    Args:
        text_to_redact: The input text to analyze and redact.

    Returns:
        A result object with the redacted text.
    """
    client = get_azure_content_safety_client()
    
    # Example: Create a blocklist for redaction
    # In a real app, this would be managed in the Azure AI Studio
    blocklist_name = "example-internal-terms"
    blocklist_description = "Internal project codenames to redact."
    
    try:
        # The API for managing blocklists is part of the client
        # This is a simplified representation of adding terms
        client.add_or_update_text_blocklist(
            blocklist_name=blocklist_name,
            blocklist=TextBlocklist(
                blocklist_name=blocklist_name,
                description=blocklist_description,
                blocklist_items=[
                    {"text": "ProjectTitan"},
                    {"text": "AlphaLaunch"}
                ]
            )
        )
        
        request = AnalyzeTextOptions(text=text_to_redact, blocklist_names=[blocklist_name], break_by_blocklists=True)
        response = client.analyze_text(request)

        redacted_text = text_to_redact
        redactions_made = 0
        if response.blocklists_match:
            # Sort by offset descending to avoid index shifting during replacement
            matches = sorted(response.blocklists_match, key=lambda x: x.offset, reverse=True)
            redactions_made = len(matches)
            for match in matches:
                start, length = match.offset, match.length
                redacted_text = redacted_text[:start] + '[REDACTED]' + redacted_text[start+length:]
        
        return RedactionResult(redacted_text=redacted_text, redactions_made=redactions_made)

    except HttpResponseError as e:
        # Handle API errors gracefully
        return RedactionResult(redacted_text=f"Error during Azure redaction: {e.message}", redactions_made=0)

