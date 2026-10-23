import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def redact_unsafe(text: str, severity_threshold: int = 4):
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    request = AnalyzeTextOptions(text=text, categories=[
        TextCategory.VIOLENCE,
        TextCategory.HATE_SPEECH,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM
    ], output_type="FourPoint")

    response = client.analyze_text(request)
    
    # This is a placeholder for actual redaction. Azure Content Safety doesn't offer direct redaction
    # but provides severity scores. Client-side logic would be needed to redact based on spans/categories.
    # For this example, we'll just indicate if redaction would be needed.
    
    needs_redaction = False
    redacted_text = text # Placeholder, as actual redaction requires more sophisticated text manipulation based on offsets

    for category in response.categories_analysis:
        if category.severity >= severity_threshold:
            needs_redaction = True
            # In a real scenario, you'd integrate with a tokenization and redaction library
            # to replace specific words or phrases identified as unsafe based on the analysis.
            # For now, we'll just conceptually mark the text for redaction.
            
    return {"original_text": text, "needs_redaction": needs_redaction, "redacted_text_placeholder": "<REDACTED_CONTENT>" if needs_redaction else text}
