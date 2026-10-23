import os

from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import get_azure_document_intelligence_client, get_document_bytes


def extract_receipt_fields(source):
    client = get_azure_document_intelligence_client()
    poller = client.begin_analyze_document(
        "prebuilt-receipt",
        AnalyzeDocumentRequest(bytes_source=get_document_bytes(source)),
    )
    result = poller.result()
    receipt = result.documents[0].fields if result.documents else {}
    items = []
    for item in (
        (receipt.get("Items") or {}).value_array
        if hasattr(receipt.get("Items"), "value_array")
        else []
    ):
        fields = item.value_object
        items.append(
            {
                "description": getattr(fields.get("Description"), "content", None),
                "quantity": getattr(fields.get("Quantity"), "content", None),
                "total": getattr(fields.get("TotalPrice"), "content", None),
            }
        )
    return {
        "merchant": getattr(receipt.get("MerchantName"), "content", None),
        "tax": getattr(receipt.get("TotalTax"), "content", None),
        "total": getattr(receipt.get("Total"), "content", None),
        "items": items,
    }


if __name__ == "__main__":
    path = os.environ.get("DOCUMENT_PATH")
    if path:
        print(extract_receipt_fields(path))
