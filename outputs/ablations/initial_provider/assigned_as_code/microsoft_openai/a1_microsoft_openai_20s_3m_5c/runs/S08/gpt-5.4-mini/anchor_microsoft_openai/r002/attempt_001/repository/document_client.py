import os
from dataclasses import dataclass

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@dataclass
class DocumentClientConfig:
    endpoint: str
    api_key: str
    model_id: str = "prebuilt-read"


def load_document_client_config(config=None):
    config = config or {}
    return DocumentClientConfig(
        endpoint=config.get("endpoint") or os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
        api_key=config.get("api_key") or os.environ["AZURE_DOCUMENT_INTELLIGENCE_API_KEY"],
        model_id=config.get("model_id") or config.get("model") or "prebuilt-read",
    )


def open_document_client(config=None):
    cfg = load_document_client_config(config)
    return DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.api_key)), cfg


def document_bytes_payload(payload):
    return payload["document_bytes"], payload["mime_type"]
