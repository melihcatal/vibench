import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions

def redact_unsafe(text: str, redaction_placeholder: str = "[REDACTED]") -> str:
    """
    Flags or redacts unsafe spans from text using Azure AI Content Safety.
    If any category has a severity of 4 (highest), the text is considered unsafe and replaced.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    is_unsafe = False
    for category in response.categories_analysis:
        if category.severity == 4: # Severity 4 often indicates highly unsafe content
            is_unsafe = True
            break
    
    if is_unsafe:
        return redaction_placeholder
    else:
        return text

if __name__ == '__main__':
    # Example usage
    # Set environment variables AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY
    unsafe_text = "I want to harm myself and others."
    safe_text = "Hello, how are you today?"

    print(f"Original: '{unsafe_text}' -> Redacted: '{redact_unsafe(unsafe_text)}'")
    print(f"Original: '{safe_text}' -> Redacted: '{redact_unsafe(safe_text)}'")
