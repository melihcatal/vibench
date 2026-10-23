import os
from storage_client import get_storage_client
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat
from azure.core.credentials import AzureKeyCredential

def run_ocr_on_stored_document(bucket_name: str, object_key: str, model_id: str = "prebuilt-read") -> dict:
    """
    Runs OCR on a stored document using Azure AI Document Intelligence.
    Requires AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not set.")

    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_key)
    document_bytes = blob.download_as_bytes()

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    poller = document_intelligence_client.begin_analyze_document(
        model_id=model_id,
        analyze_request=AnalyzeDocumentRequest(bytes_source=document_bytes),
        content_type="application/octet-stream",
        output_content_format=ContentFormat.MARKDOWN
    )

    result = poller.result()
    return {
        "content": result.content,
        "pages": len(result.pages),
        "tables": len(result.tables) if result.tables else 0
    }