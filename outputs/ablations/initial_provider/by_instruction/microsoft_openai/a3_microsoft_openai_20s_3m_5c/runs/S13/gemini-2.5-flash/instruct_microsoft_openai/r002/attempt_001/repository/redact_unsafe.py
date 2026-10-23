import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def redact_unsafe(text: str, redaction_character: str = "*") -> str:
    """
    Flags or redacts unsafe spans from text using Azure Content Safety.
    This example will just flag by severity, not actual spans, as the service
    does not directly return spans for redaction in the same way as PII.
    For true span-based redaction, a custom solution or a service specifically
    offering that feature would be needed, potentially based on the offset/length
    of detected unsafe terms if the service provided them.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    # The Content Safety service primarily provides severity scores per category.
    # It does not directly provide character offsets for unsafe spans to perform direct redaction.
    # For demonstration, we will consider any text with a high severity in any category as 'unsafe'
    # and replace the entire text for simplicity, or indicate that it should be reviewed.
    # A more sophisticated redaction would require a service that returns span information (start/end index).
    
    request = AnalyzeTextOptions(text=text, categories=[
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ], blocklist_names=[])

    response = client.analyze_text(request)
    
    # Determine if any category has a high severity
    is_unsafe_overall = False
    for category_result in response.categories_analysis:
        # Assuming a severity of 4 or more (out of 0-7) implies a need for redaction/review
        if category_result.severity >= 4:
            is_unsafe_overall = True
            break

    if is_unsafe_overall:
        # In a real scenario, you might have a more granular redaction based on specific terms
        # or phrases identified, if the API supported returning their locations.
        # For this example, if the text is deemed unsafe, we return a redacted placeholder.
        return redaction_character * len(text) # Simple full text redaction
    else:
        return text
