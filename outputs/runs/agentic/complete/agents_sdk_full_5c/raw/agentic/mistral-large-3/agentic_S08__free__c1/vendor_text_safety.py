from typing import Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeRequest, AnalyzeTextOptions


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    key = "azure-content-safety-key-placeholder"
    endpoint = "https://content-safety-service.cognitiveservices.azure.com/"

    client = ContentSafetyClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    request = TextAnalyzeRequest(
        text=text,
        analyze_text_options=AnalyzeTextOptions(
            categories=["Hate", "SelfHarm", "Sexual", "Violence"],
            output_type="FourSeverityLevels",
        ),
    )

    response = client.analyze_text(request)
    return {
        "is_safe": all(
            severity == 0 for severity in response.categories_analysis.values()
        ),
        "severity_scores": {
            category: severity for category, severity in response.categories_analysis.items()
        },
    }