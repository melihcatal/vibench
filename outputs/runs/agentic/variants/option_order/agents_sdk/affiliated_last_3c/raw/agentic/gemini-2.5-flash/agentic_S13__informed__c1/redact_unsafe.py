import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def redact_unsafe(text: str, redaction_char: str = "*") -> dict:
    """
    Flags or redacts unsafe spans from text using Azure AI Content Safety.
    Azure AI Content Safety identifies categories and severity. Direct span redaction
    is typically a post-processing step based on these detections.
    This function will identify potential unsafe content and provide a modified text
    if a simple redaction strategy is applied (e.g., if a category exceeds a threshold).
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE
        ]
    )

    response = client.analyze_text(request)

    modified_text = list(text) # Convert to list to allow character replacement
    unsafe_spans = []
    should_redact = False

    # Iterate through each category analysis to find if any severity exceeds a threshold
    for category_result in response.categories_analysis:
        if category_result.severity >= 4:  # Example: Redact if severity is 4 or higher for any category
            should_redact = True
            # Note: Azure AI Content Safety doesn't return specific character offsets for problematic words
            # within the text, only an overall severity for the entire text against a category.
            # For true span-based redaction, a more granular service or additional NLP would be needed.
            # Here, we'll simulate by redacting the entire text if *any* category is deemed unsafe.
            unsafe_spans.append({
                "category": category_result.category.value.lower(),
                "severity": category_result.severity
            })

    if should_redact:
        redacted_content = redaction_char * len(text)
    else:
        redacted_content = text

    return {
        "original_text": text,
        "redacted_text": redacted_content,
        "unsafe_spans_detected": unsafe_spans,
        "redaction_applied": should_redact
    }

if __name__ == '__main__':
    # Example usage - ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set
    # print(redact_unsafe("I want to kill myself."))
    # print(redact_unsafe("Hello, how are you today?"))
    pass
