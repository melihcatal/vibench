import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeOptions, TextCategory, TextBlocklistMatch

def redact_unsafe(text: str, blocklist_names: list = None):
    """
    Flags or redacts unsafe spans from text using Azure AI Content Safety.
    Note: Azure Content Safety primarily flags categories and severity.
    For redaction based on specific terms, blocklists can be used, but
    direct redaction of detected unsafe categories is typically done client-side
    based on the analysis result. This example focuses on analysis.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = TextAnalyzeOptions(text=text, categories=[
        TextCategory.VIOLENCE,
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
    ])
    if blocklist_names:
        request.blocklist_names = blocklist_names

    response = client.analyze_text(request)

    redacted_text = list(text) # Convert to list for mutable character replacement

    flags = []
    for category_result in response.categories_analysis:
        if category_result.severity > 0: # Assuming severity > 0 indicates unsafe content
            flags.append({
                "type": "category",
                "category": category_result.category.value,
                "severity": category_result.severity
            })

    if response.blocklist_matches:
        for match in response.blocklist_matches:
            flags.append({
                "type": "blocklist_match",
                "blocklist_name": match.blocklist_name,
                "text": match.text,
                "offset": match.offset,
                "length": match.length
            })
            # Example redaction: replace matched blocklist terms with '*'
            for i in range(match.offset, match.offset + match.length):
                if i < len(redacted_text):
                    redacted_text[i] = '*'

    return {
        "original_text": text,
        "redacted_text": "".join(redacted_text),
        "flags": flags
    }

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY to be set)
    # text_to_redact = "This is a test with a badword. And another bad phrase."
    # # Ensure a blocklist with "badword" and "bad phrase" exists in your Azure Content Safety resource
    # # or call the API to create one. For this example, we just show the call.
    # redaction_output = redact_unsafe(text_to_redact, blocklist_names=["myblocklist"])
    # print(redaction_output)
    pass
