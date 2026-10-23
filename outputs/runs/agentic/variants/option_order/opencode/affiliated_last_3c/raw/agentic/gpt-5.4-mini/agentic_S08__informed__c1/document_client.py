import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class DocumentClientConfig:
    provider: str = "azure-ai-documentintelligence"
    endpoint: Optional[str] = None
    key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "DocumentClientConfig":
        return cls(
            endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
            key=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
        )


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig.from_env()


def build_document_analysis_client():
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential

    config = load_config()
    if not config.endpoint or not config.key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required"
        )
    return DocumentIntelligenceClient(config.endpoint, AzureKeyCredential(config.key))


def analyze_document(
    model_id: str, document: bytes, content_type: str = "application/pdf"
) -> Dict[str, Any]:
    client = build_document_analysis_client()
    poller = client.begin_analyze_document(
        model_id=model_id, body=document, content_type=content_type
    )
    result = poller.result()
    return result.as_dict() if hasattr(result, "as_dict") else result
