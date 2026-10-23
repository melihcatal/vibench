import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeOptions, TextCategory

def redact_unsafe(text: str, redaction_char: str = "*") -> dict:
    """
    Flags unsafe content in text and suggests redaction based on Azure AI Content Safety analysis.
    Azure AI Content Safety provides categories and severities. Actual redaction of specific spans
    would typically require custom logic or a service that returns offset/length of unsafe spans.
    This function returns the analysis and a 'redacted_text' placeholder for demonstration.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Azure AI Content Safety does not natively return character offsets for redaction in its SDK.
    # It provides category-level severity. For true redaction, one might use an LLM or a different service.
    # For this example, we will just indicate if the text *should* be redacted.
    request = TextAnalyzeOptions(text=text, categories=[
        TextCategory.HATE_SPEECH,
        TextCategory.VIOLENCE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
    ])

    response = client.analyze_text(request)

    analysis_result = {}
    should_redact = False
    if response.categories_analysis:
        for category in response.categories_analysis:
            analysis_result[category.category] = {
                "severity": category.severity,
                "violated": category.violated if hasattr(category, 'violated') else None
            }
            if category.violated:
                should_redact = True
    
    # Simulate redaction: if any category is violated, replace the whole text (or indicate full redaction)
    redacted_text = redaction_char * len(text) if should_redact else text

    return {"original_text": text, "analysis": analysis_result, "should_redact": should_redact, "redacted_text": redacted_text}

if __name__ == '__main__':
    # Example usage (requires setting environment variables)
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_KEY"
    #
    # unsafe_text = "I want to harm myself."
    # mild_unsafe_text = "This is a bit suggestive."
    # safe_text = "Enjoy your day."
    #
    # print(f"Redaction for unsafe text: {redact_unsafe(unsafe_text)}")
    # print(f"Redaction for mild unsafe text: {redact_unsafe(mild_unsafe_text)}")
    # print(f"Redaction for safe text: {redact_unsafe(safe_text)}")
