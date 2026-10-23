from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from storage_client import get_blob_service_client, get_container_name, load_storage_config
from storage_models import OCRResult


def stored_document_ocr(container_name: str, object_name: str) -> OCRResult:
    cfg = load_storage_config()
    blob = get_blob_service_client().get_blob_client(get_container_name(container_name), object_name)
    analyzer = DocumentAnalysisClient(endpoint=cfg.account_url, credential=AzureKeyCredential(cfg.credential or ""))
    url = blob.url
    result = analyzer.begin_analyze_document_from_url("prebuilt-read", url).result()
    text = "\n".join([line.content for page in result.pages for line in page.lines])
    return OCRResult(text=text, raw={"model_id": "prebuilt-read"})
