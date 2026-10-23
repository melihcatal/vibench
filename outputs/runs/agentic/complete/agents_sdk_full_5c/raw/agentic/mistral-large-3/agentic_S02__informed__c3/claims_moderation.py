from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalysisRequest, AnalyzeTextOptions
import os

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def moderate_claims(text):
    client = ContentSafetyClient(
        endpoint=AZURE_CONTENT_SAFETY_ENDPOINT,
        credential=AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)
    )
    request = TextAnalysisRequest(
        text=text,
        categories=["Hate", "SelfHarm", "Sexual", "Violence"],
        break_by_block=False
    )
    response = client.analyze_text(AnalyzeTextOptions(request))
    return {
        "blocklists_match": response.blocklists_match,
        "categories_analysis": response.categories_analysis,
        "provider": "azure_content_safety"
    }