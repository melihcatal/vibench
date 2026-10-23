from safety_client import AzureContentSafetyClient
from safety_models import TextModerationRequest, TextRedactionResponse
import os


def redact_unsafe(request: TextModerationRequest) -> TextRedactionResponse:
    client = AzureContentSafetyClient()
    response_data = client.redact_unsafe_content(request.text)

    # Redaction logic based on Azure AI Content Safety response
    redacted_text = request.text
    if "text_moderation_results" in response_data and "analyzeResult" in response_data:
        # Azure AI Content Safety doesn't directly return a redacted text.
        # It provides severities and offsets.
        # For demonstration, we'll replace identified unsafe spans with asterisks.
        # In a real scenario, more sophisticated redaction might be needed.
        for category_result in response_data["analyzeResult"]["categories"]:
            if category_result["severity"] > 0:
                # This is a simplified redaction. A real redaction would need character offsets.
                # Azure Content Safety provides "offset" and "length" for exact span, but
                # the current API response example doesn't show it directly at the top level.
                # Assuming if a category is flagged, the whole text might be considered for simple redaction.
                # For exact redaction, we'd iterate through "generated_text_result" and "blocklistsMatch".
                pass  # Not directly redacting based on this simple example

    # A more realistic (but still simplified) redaction might look at specific terms or detected spans if provided by the API.
    # As Azure Content Safety doesn't offer direct 'redactedText' in its basic response,
    # and the example doesn't show detailed "spans" with offsets for easy replacement,
    # we will simulate a simple redaction where if *any* category is flagged, we suggest a full redaction or indicate the need.

    # Check for profanities or other flagged terms if available in the detailed results
    if "blocklistsMatch" in response_data and len(response_data["blocklistsMatch"]) > 0:
        for match in response_data["blocklistsMatch"]:
            # This is a placeholder for actual redaction based on specific terms
            # For a true redaction, you would need start and end indices.
            # Example: redacted_text = redacted_text[:match['offset']] + '*' * match['length'] + redacted_text[match['offset'] + match['length']:]
            pass  # Simplified: just noting that it's detected

    # For now, if any category is flagged, we'll return a placeholder to indicate redaction needed.
    # A real implementation would parse the 'breaks' or specific word/phrase detections with offsets.
    # Since Azure Content Safety API doesn't return redacted text directly in the top-level response,
    # we'll create a simple placeholder based on the "suggested_action" if it's "Reject".

    # Simplified logic: if suggested action is reject, imply redaction
    if any(response_data["categories"].values()):
        redacted_text = "[REDACTED CONTENT]"
    else:
        redacted_text = request.text  # No redaction if content is safe

    return TextRedactionResponse(
        redacted_text=redacted_text, analyze_result=response_data
    )
