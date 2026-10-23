from typing import Dict, Any, Optional
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_vendor_notes(text: Optional[str]) -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using Azure Content Safety.
    """
    if not text:
        return {"is_safe": True, "categories": {}}

    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not all([endpoint, key]):
        raise ValueError("Missing Azure Content Safety environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    response = client.analyze_text(request)
    result = {
        "is_safe": True,
        "categories": {
            "hate": response.hate_result.severity if response.hate_result else 0,
            "self_harm": response.self_harm_result.severity
            if response.self_harm_result
            else 0,
            "sexual": response.sexual_result.severity if response.sexual_result else 0,
            "violence": response.violence_result.severity
            if response.violence_result
            else 0,
        },
    }

    if any(result["categories"].values()):
        result["is_safe"] = False

    return result
