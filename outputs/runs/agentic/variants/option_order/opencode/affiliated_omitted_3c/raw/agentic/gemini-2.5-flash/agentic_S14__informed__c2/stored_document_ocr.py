import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import ContentFormat, AnalyzeDocumentRequest


def run_ocr_on_document(document_url: str) -> str:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables must be set."
        )

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # The 'prebuilt-read' model is used for OCR and general document analysis.
    # You can specify other prebuilt models like 'prebuilt-layout' or custom models.
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-read",
        AnalyzeDocumentRequest(url_source=document_url),
        output_content_format=ContentFormat.MARKDOWN,
    )
    result = poller.result()

    if result.content:
        return result.content
    else:
        return "No content extracted."
