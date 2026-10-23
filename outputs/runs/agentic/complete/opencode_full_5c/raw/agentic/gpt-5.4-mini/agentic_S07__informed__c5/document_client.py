import os
from dataclasses import dataclass


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


@dataclass
class DocumentClientConfig:
    endpoint: str
    key: str


def load_document_client_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        endpoint=_env("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        key=_env("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
    )


def _client_kwargs():
    return {
        "endpoint": load_document_client_config().endpoint,
        "credential": load_document_client_config().key,
    }


def get_document_intelligence_client():
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential

    config = load_document_client_config()
    return DocumentIntelligenceClient(
        endpoint=config.endpoint, credential=AzureKeyCredential(config.key)
    )


def get_prebuilt_model_id(name: str) -> str:
    mapping = {
        "ocr": "prebuilt-read",
        "layout": "prebuilt-layout",
        "tables": "prebuilt-layout",
        "key_values": "prebuilt-layout",
        "invoice": "prebuilt-invoice",
    }
    return mapping.get(name, "prebuilt-layout")
