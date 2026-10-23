from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import os
from azure.ai.contentsafety.models import TextCategory


def redact_unsafe(text: str):
    """
    Flags or redacts unsafe spans from text using Azure AI Content Safety.
    Note: Azure AI Content Safety does not directly redact, but provides categories and severities.
    Redaction logic would be applied on the client side based on the response.
    This function will return the analysis.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = {
        "text": text,
        "blocklistNames": [],
        "breakByBlocklists": False,
        "categories": [
            TextCategory.VIOLENCE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.HATE,
        ],
        "outputType": "FourSeverityLevels",
    }
    response = client.analyze_text(request)

    return response.to_dict()
