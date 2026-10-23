from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalysisRequest, AnalyzeTextOptions
import os
from typing import Dict, Any

endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
client = ContentSafetyClient(endpoint, AzureKeyCredential(key))


def message_safety(text: str) -> Dict[str, Any]:
    request = TextAnalysisRequest(text=text)
    options = AnalyzeTextOptions(
        categories=["Hate", "SelfHarm", "Sexual", "Violence"],
        output_type="EightSeverityLevels",
    )
    response = client.analyze_text(request, options)
    return {
        "is_safe": all(
            getattr(response, category).severity == 0
            for category in [
                "hate_result",
                "self_harm_result",
                "sexual_result",
                "violence_result",
            ]
        ),
        "results": {
            "hate": response.hate_result.severity,
            "self_harm": response.self_harm_result.severity,
            "sexual": response.sexual_result.severity,
            "violence": response.violence_result.severity,
        },
    }
