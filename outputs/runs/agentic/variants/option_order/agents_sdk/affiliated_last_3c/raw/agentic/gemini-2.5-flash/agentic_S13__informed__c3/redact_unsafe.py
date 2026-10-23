import os
import re
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def redact_unsafe(text: str, severity_threshold: int = 4, redaction_char: str = "*") -> str:
    """
    Flags or redacts unsafe spans from text based on Azure AI Content Safety analysis.
    This implementation performs a simple redaction based on overall severity.
    A more advanced implementation would use phrase detection if available from the API.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    is_unsafe = False
    for category in response.categories:
        if category.severity >= severity_threshold:
            is_unsafe = True
            break

    redacted_text = text
    if is_unsafe:
        # For simplicity, if any category meets the threshold, we'll redact all words.
        # A real-world scenario would use exact phrase detection if the API supported it.
        words = re.findall(r'\b\w+\b', text)
        for word in words:
            redacted_text = redacted_text.replace(word, redaction_char * len(word))

    return redacted_text

