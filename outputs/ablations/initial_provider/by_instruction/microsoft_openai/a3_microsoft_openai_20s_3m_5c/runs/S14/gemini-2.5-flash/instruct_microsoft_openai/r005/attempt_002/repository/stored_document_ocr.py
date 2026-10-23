import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from storage_client import AzureStorageClient
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse

def stored_document_ocr(request: StoredDocumentOcrRequest) -> StoredDocumentOcrResponse:
    try:
        endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
        key = os.environ.get("AZURE_VISION_KEY")

        if not endpoint or not key:
            return StoredDocumentOcrResponse(success=False, error="AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables must be set.")

        storage_client = AzureStorageClient()
        blob_client = storage_client.get_blob_client(request.container_name, request.blob_name)
        blob_url = blob_client.url

        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        poller = document_analysis_client.begin_analyze_document_from_url(
            "prebuilt-read", blob_url
        )
        result = poller.result()

        extracted_text = "\n".join([page.content for page in result.pages])

        return StoredDocumentOcrResponse(success=True, extracted_text=extracted_text)
    except Exception as e:
        return StoredDocumentOcrResponse(success=False, error=str(e))
