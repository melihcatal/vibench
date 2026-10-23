import os
import json
import requests
from typing import Optional, Dict, Any, List
from document_client import get_azure_document_intelligence_config, read_document_bytes
from document_models import InvoiceExtraction, LineItem


AZURE_DI_ENDPOINT = "https://documentintelligence.cognitiveservices.azure.com/"
AZURE_DI_MODEL_ID = "prebuilt-invoice"
AZURE_DI_API_VERSION = "2023-07-31"


def extract_invoice_fields(file_path: str) -> InvoiceExtraction:
    config = get_azure_document_intelligence_config()
    endpoint = config["endpoint"].rstrip("/")
    api_key = config["api_key"]
    model_id = config.get("model_id", AZURE_DI_MODEL_ID)
    api_version = config.get("api_version", AZURE_DI_API_VERSION)

    analyze_url = f"{endpoint}/documentintelligence/documentModels/{model_id}:analyze?api-version={api_version}"

    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/pdf"}

    document_bytes = read_document_bytes(file_path)

    response = requests.post(analyze_url, headers=headers, data=document_bytes)
    response.raise_for_status()

    operation_location = response.headers["Operation-Location"]

    result_url = f"{operation_location}&api-version={api_version}"
    get_result_headers = {"Ocp-Apim-Subscription-Key": api_key}

    import time

    max_retries = 30
    for _ in range(max_retries):
        result_response = requests.get(result_url, headers=get_result_headers)
        result_response.raise_for_status()
        result_data = result_response.json()

        if result_data.get("status") == "succeeded":
            break
        elif result_data.get("status") == "failed":
            raise RuntimeError(
                f"Azure Document Intelligence analysis failed: {result_data.get('error')}"
            )
        time.sleep(2)
    else:
        raise TimeoutError("Azure Document Intelligence analysis timed out")

    return parse_azure_invoice_response(result_data)


def parse_azure_invoice_response(result_data: Dict[str, Any]) -> InvoiceExtraction:
    documents = result_data.get("analyzeResult", {}).get("documents", [])
    if not documents:
        raise ValueError("No documents found in Azure Document Intelligence response")

    doc = documents[0]
    fields = doc.get("fields", {})

    vendor_name = _extract_field_value(fields, "VendorName", str, "")
    invoice_date = _extract_field_value(fields, "InvoiceDate", str, "")
    invoice_number = _extract_field_value(fields, "InvoiceId", str, "")
    total_amount = _extract_field_value(fields, "InvoiceTotal", float, 0.0)
    tax_amount = _extract_field_value(fields, "TotalTax", float, 0.0)
    currency = _extract_field_value(fields, "CurrencyCode", str, "USD")

    confidence_scores = {}
    for field_name in [
        "VendorName",
        "InvoiceDate",
        "InvoiceId",
        "InvoiceTotal",
        "TotalTax",
    ]:
        if field_name in fields:
            confidence_scores[field_name] = fields[field_name].get("confidence", 0.0)

    line_items = []
    items_field = fields.get("Items", {})
    items_value = items_field.get("valueArray", {}).get("valueArray", [])
    if not items_value:
        items_value = items_field.get("valueArray", [])

    for item_obj in items_value:
        item_fields = item_obj.get("valueObject", {})
        line_item = LineItem(
            description=_extract_field_value(item_fields, "Description", str, ""),
            quantity=_extract_field_value(item_fields, "Quantity", float, 0.0),
            unit_price=_extract_field_value(item_fields, "UnitPrice", float, 0.0),
            total=_extract_field_value(item_fields, "Amount", float, 0.0),
        )
        line_items.append(line_item)

    return InvoiceExtraction(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        invoice_number=invoice_number,
        total_amount=total_amount,
        tax_amount=tax_amount,
        currency=currency,
        line_items=line_items,
        confidence_scores=confidence_scores,
        raw_response=result_data,
    )


def _extract_field_value(fields: Dict[str, Any], field_name: str, cast_type, default):
    field_obj = fields.get(field_name, {})
    value = field_obj.get("value", default)
    if value is None:
        return default
    try:
        return cast_type(value)
    except (ValueError, TypeError):
        return default


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        result = extract_invoice_fields(sys.argv[1])
        print(
            json.dumps(
                {
                    "vendor_name": result.vendor_name,
                    "invoice_date": result.invoice_date,
                    "invoice_number": result.invoice_number,
                    "total_amount": result.total_amount,
                    "tax_amount": result.tax_amount,
                    "currency": result.currency,
                    "line_items_count": len(result.line_items),
                    "confidence_scores": result.confidence_scores,
                },
                indent=2,
            )
        )
