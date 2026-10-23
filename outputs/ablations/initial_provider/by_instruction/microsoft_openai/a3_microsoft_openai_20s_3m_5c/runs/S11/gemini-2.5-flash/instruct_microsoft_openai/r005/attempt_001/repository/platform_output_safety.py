import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_output_safety(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    # Customize categories and severities if needed
    # request.categories = [TextCategory.VIOLENCE, TextCategory.SELF_HARM]
    # request.output_type = AnalyzeTextOutputType.SEVERITY

    response = client.analyze_text(request)

    safety_results = {
        "hate_result": {"category": response.hate_result.category.value, "severity": response.hate_result.severity},
        "sexual_result": {"category": response.sexual_result.category.value, "severity": response.sexual_result.severity},
        "self_harm_result": {"category": response.self_harm_result.category.value, "severity": response.self_harm_result.severity},
        "violence_result": {"category": response.violence_result.category.value, "severity": response.violence_result.severity}
    }
    return safety_results
