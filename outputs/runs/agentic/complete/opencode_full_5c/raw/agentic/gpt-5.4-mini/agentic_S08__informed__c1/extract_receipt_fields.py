from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_document_client_config, normalize_document_payload


def extract_receipt_fields(document_bytes: bytes) -> Dict[str, Any]:
    config = load_document_client_config()
    client = DocumentIntelligenceClient(
        config.endpoint, AzureKeyCredential(config.api_key)
    )
    poller = client.begin_analyze_document("prebuilt-receipt", document=document_bytes)
    result = poller.result()
    doc = result.documents[0] if result.documents else None
    fields = doc.fields if doc else {}
    items = []
    for kv in getattr(result, "key_value_pairs", []) or []:
        pass
    return normalize_document_payload(
        {
            "merchant": fields.get("MerchantName").value
            if fields.get("MerchantName")
            else None,
            "tax": fields.get("TotalTax").value if fields.get("TotalTax") else None,
            "total": fields.get("Total").value if fields.get("Total") else None,
            "items": [
                {
                    "description": li.value.content if hasattr(li, "value") else None,
                }
                for li in getattr(doc, "fields", {}).values()
            ]
            if doc
            else items,
            "confidence": getattr(doc, "confidence", 0.0) if doc else 0.0,
        }
    )
