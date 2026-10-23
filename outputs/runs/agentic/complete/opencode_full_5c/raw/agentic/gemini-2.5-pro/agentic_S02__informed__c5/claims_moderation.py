from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from identity_client import identity_client


def moderate_claim_text(text: str) -> dict:
    """
    Moderates a free-text claim using Azure AI Content Safety.
    """
    if not text:
        return {"is_safe": True, "analysis": {}}

    client = ContentSafetyClient(
        identity_client.AZURE_CONTENT_SAFETY_ENDPOINT,
        AzureKeyCredential(identity_client.AZURE_CONTENT_SAFETY_KEY),
    )

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Error moderating text with Azure Content Safety: {e}")
        return {"is_safe": False, "error": str(e)}

    analysis = {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "self_harm": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity
        if response.violence_result
        else 0,
    }

    is_safe = all(severity == 0 for severity in analysis.values())

    return {"is_safe": is_safe, "analysis": analysis}
