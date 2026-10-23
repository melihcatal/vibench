from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import os


def moderate_text(text: str):
    """
    Scores user text for unsafe or policy-violating content using Azure AI Content Safety.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = {"text": text}
    response = client.analyze_text(request)

    return response.to_dict()
