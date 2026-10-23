# [LATER-STEP] vendor_text_safety.py
"""
Moderate vendor notes or memo fields using Azure Content Safety API.
"""
import json
from azure.ai.contentsafety import ContentSafetyClient
from document_models import InvoiceExtractionResponse

def moderate_vendor_notes(extracted: InvoiceExtractionResponse) -> InvoiceExtractionResponse:
    """Run vendor memo through content safety filter; replace unsafe content.

    Args:
        extracted: Dict from upstream invoice extraction.

    Returns:
        Updated dict with any flagged text sanitized.
    """
    endpoint = "https://<YOUR_RESOURCE>.cognitiveservices.azure.com/"
    credential = "<YOUR_KEY>"
    client = ContentSafetyClient(endpoint=endpoint, credential=credential)
    content = extracted.get("vendor", "")
    # Call moderation API (placeholder)
    result = client.moderate_text(content=content, category=["sexual","selfHarm","suicide","violence","hate","selfImage","drugTrafficking","drugUse","dangerousLanguage","abuse","spam"])
    safe = result.flagged_content  # placeholder: assume sanitized version returned
    if safe != content:
        extracted["vendor"] = safe
    return extracted
