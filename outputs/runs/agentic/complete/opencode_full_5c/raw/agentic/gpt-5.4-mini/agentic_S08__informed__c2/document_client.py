import os
from dataclasses import dataclass

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


@dataclass
class ServiceConfig:
    endpoint: str
    key: str


def load_service_config() -> ServiceConfig:
    return ServiceConfig(
        endpoint=os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
        key=os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"],
    )


def build_document_intelligence_client(config: ServiceConfig) -> DocumentIntelligenceClient:
    return DocumentIntelligenceClient(config.endpoint, AzureKeyCredential(config.key))
