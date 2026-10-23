import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

def analyze_document_from_url(document_url: str) -> str:
    """
    Analyzes a document from a URL using Azure AI Document Intelligence
    and returns the extracted text content.

    Args:
        document_url (str): The publicly accessible URL of the document to analyze.

    Returns:
        str: The concatenated text content from the document.
    """
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Document Intelligence credentials not found in environment variables."
        )

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-read", {"urlSource": document_url}
    )
    result: AnalyzeResult = poller.result()

    if result.content:
        return result.content
    return ""
