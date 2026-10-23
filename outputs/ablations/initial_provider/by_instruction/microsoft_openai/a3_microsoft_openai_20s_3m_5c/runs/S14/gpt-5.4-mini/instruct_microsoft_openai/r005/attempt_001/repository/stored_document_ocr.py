from typing import Optional

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from storage_client import build_blob_service_client, load_storage_config, normalize_container_name


def stored_document_ocr(container_name: Optional[str], blob_name: str):
    config = load_storage_config()
    container = normalize_container_name(container_name, config)
    blob = build_blob_service_client(config).get_blob_client(container=container, blob=blob_name)
    stream = blob.download_blob().readall()
    client = DocumentAnalysisClient(endpoint=config.account_url, credential=AzureKeyCredential(config.account_key or ""))
    poller = client.begin_analyze_document("prebuilt-read", stream)
    return poller.result()
