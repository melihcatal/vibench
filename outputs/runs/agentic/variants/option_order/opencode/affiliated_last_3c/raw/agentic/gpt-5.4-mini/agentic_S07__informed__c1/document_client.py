import os
from dataclasses import dataclass


@dataclass
class DocumentServiceConfig:
    endpoint: str
    key: str
    model_id: str


def load_config() -> DocumentServiceConfig:
    return DocumentServiceConfig(
        endpoint=os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", ""),
        key=os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", ""),
        model_id=os.environ.get(
            "AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-read"
        ),
    )


def make_client():
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential

    config = load_config()
    return DocumentIntelligenceClient(config.endpoint, AzureKeyCredential(config.key))
