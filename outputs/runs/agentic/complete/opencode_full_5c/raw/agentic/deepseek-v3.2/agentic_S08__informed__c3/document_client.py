import os
from typing import Optional
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential


def get_azure_document_intelligence_client() -> DocumentIntelligenceClient:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Missing Azure Document Intelligence credentials. "
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables."
        )

    credential = AzureKeyCredential(key)
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=credential)
    return client


def create_analyze_request(
    file_path: str, model_id: str = "prebuilt-invoice"
) -> AnalyzeDocumentRequest:
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    return AnalyzeDocumentRequest(
        base64_source=file_bytes,
        features=["keyValuePairs", "styleFont"],
        model_id=model_id,
    )


def get_model_id_for_document_type(doc_type: str) -> str:
    model_map = {
        "invoice": "prebuilt-invoice",
        "receipt": "prebuilt-receipt",
        "id": "prebuilt-idDocument",
        "business_card": "prebuilt-businessCard",
        "layout": "prebuilt-layout",
    }
    return model_map.get(doc_type, "prebuilt-layout")
