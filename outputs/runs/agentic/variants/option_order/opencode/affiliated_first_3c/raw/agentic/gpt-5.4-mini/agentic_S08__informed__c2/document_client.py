import os
from typing import Any, Dict, Iterable, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def build_azure_di_client() -> DocumentIntelligenceClient:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def first_nonempty(fields: Dict[str, Any], names: Iterable[str]) -> Any:
    for name in names:
        value = fields.get(name)
        if value not in (None, '', [], {}):
            return getattr(value, 'value', value)
    return None
