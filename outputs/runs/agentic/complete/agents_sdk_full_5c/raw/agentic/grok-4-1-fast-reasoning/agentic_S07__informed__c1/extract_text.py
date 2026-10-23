from document_client import document_client
from document_models import normalize_text
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

def extract_text(image_bytes: bytes) -> str:
    request = AnalyzeDocumentRequest(bytes=image_bytes)
    poller = document_client.begin_analyze_document(
        model_id="prebuilt-read",
        document=request
    )
    result = poller.result()
    return normalize_text(result)