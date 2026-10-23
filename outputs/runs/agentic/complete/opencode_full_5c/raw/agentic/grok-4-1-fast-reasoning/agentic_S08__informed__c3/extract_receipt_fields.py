import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult


def extract_receipt_fields(pdf_path: str) -> dict:
    """
    Extract structured fields from a receipt PDF using Azure Document Intelligence prebuilt-receipt.
    Returns dict with merchant, tax, total, date, items.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY required."
        )

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(pdf_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-receipt", document=f.read(), content_type="application/pdf"
        )
    result: AnalyzeResult = poller.result()

    field_dict = result.field_dict

    merchant_field = field_dict.get("MerchantName")
    merchant = {
        "value": merchant_field.content if merchant_field else "",
        "confidence": merchant_field.confidence if merchant_field else 0.0,
    }

    date_field = field_dict.get("TransactionDate")
    date_dict = {
        "value": date_field.content if date_field else "",
        "confidence": date_field.confidence if date_field else 0.0,
    }

    tax_field = field_dict.get("TaxTotal")
    tax_dict = {
        "value": tax_field.content if tax_field else "",
        "confidence": tax_field.confidence if tax_field else 0.0,
    }

    total_field = field_dict.get("Total")
    total_dict = {
        "value": total_field.content if total_field else "",
        "confidence": total_field.confidence if total_field else 0.0,
    }

    items = []
    items_field = field_dict.get("Items")
    if items_field and hasattr(items_field, "value_array") and items_field.value_array:
        for item_field in items_field.value_array:
            desc = ""
            qty = None
            price = None
            amt = 0.0
            if hasattr(item_field, "value_dict"):
                name_field = item_field.value_dict.get("Name")
                if name_field:
                    desc = name_field.content or ""
                qty_field = item_field.value_dict.get("Quantity")
                if qty_field:
                    qty = float(qty_field.content) if qty_field.content else None
                price_field = item_field.value_dict.get("Price")
                if price_field:
                    price = float(price_field.content) if price_field.content else None
                total_field_item = item_field.value_dict.get("Total")
                if total_field_item:
                    amt = (
                        float(total_field_item.content)
                        if total_field_item.content
                        else 0.0
                    )
            items.append(
                {
                    "description": desc,
                    "quantity": qty,
                    "unit_price": price,
                    "amount": amt,
                }
            )

    return {
        "merchant": merchant,
        "tax": tax_dict,
        "total": total_dict,
        "date": date_dict,
        "items": items,
    }
