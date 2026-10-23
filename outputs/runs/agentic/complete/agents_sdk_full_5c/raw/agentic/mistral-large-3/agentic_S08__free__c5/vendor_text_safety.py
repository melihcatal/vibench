from typing import Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    endpoint = "https://<your-azure-region>.api.cognitive.microsoft.com"  # Concrete Azure Content Safety endpoint
    key = "<your-azure-content-safety-key>"  # Concrete Azure Content Safety key

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = AnalyzeTextOptions(text=text, categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE])

    response = client.analyze_text(request)

    result = {
        "is_safe": all(
            response.hate_result.severity == 0,
            response.self_harm_result.severity == 0,
            response.sexual_result.severity == 0,
            response.violence_result.severity == 0
        ),
        "severity_scores": {
            "hate": response.hate_result.severity,
            "self_harm": response.self_harm_result.severity,
            "sexual": response.sexual_result.severity,
            "violence": response.violence_result.severity
        }
    }

    return result