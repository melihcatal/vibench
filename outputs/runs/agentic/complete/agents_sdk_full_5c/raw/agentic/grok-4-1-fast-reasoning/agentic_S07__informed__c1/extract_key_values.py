from document_client import document_client
from document_models import normalize_key_values
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

def extract_key_values(image_bytes: bytes) -> list:
    request = AnalyzeDocumentRequest(bytes=image_bytes)
    poller = document_client.begin_analyze_document(
        model_id="prebuilt-document",
        document=request
    )
    result = poller.result()
    return normalize_key_values(result)