from safety_client import get_content_safety_client
from safety_models import TextModerationResponse
from azure.ai.contentsafety.models import AnalyzeTextContentItem


def redact_unsafe_text(text: str, redaction_string: str = "[REDACTED]") -> str:
    """
    Flags or redacts unsafe spans from text using Azure AI Content Safety.
    This implementation redacts the entire text if any category exceeds severity 0.
    For more granular redaction, further parsing of the Content Safety API response would be needed.
    """
    client = get_content_safety_client()

    request = AnalyzeTextContentItem(text=text)
    response = client.analyze_text(text_item=request)

    redacted_text = text

    if response.categories_analysis:
        for category_analysis in response.categories_analysis:
            # If any category has a severity greater than 0, redact the entire text for simplicity
            # A more advanced implementation would use block_lists_match and analyze_text_with_blocklists
            # or custom logic to redact specific spans if provided by the service.
            if category_analysis.severity > 0:
                return redaction_string  # Simple full text redaction

    return redacted_text
