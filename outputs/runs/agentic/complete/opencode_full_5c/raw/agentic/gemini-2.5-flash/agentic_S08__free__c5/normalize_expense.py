import json
from typing import Dict, Any, Union
from document_client import get_generative_model_client
from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpense,
)
import datetime


def normalize_expense(
    project_id: str,
    location: str,
    document_type: str,
    extracted_data: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    original_document_id: str = None,
) -> NormalizedExpense:
    model = get_generative_model_client(project_id, location)

    # Prepare a simplified dictionary from the Pydantic model for the LLM
    # We'll pass confidence scores separately or handle them after LLM response
    if isinstance(extracted_data, InvoiceExtractionResult):
        raw_data_dict = {
            "document_type": "invoice",
            "vendor_name": extracted_data.vendor_name.value,
            "invoice_date": extracted_data.invoice_date.value,
            "total_amount": extracted_data.total_amount.value,
            "currency": extracted_data.currency.value,
            "line_items": [
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price,
                    "currency": item.currency,
                }
                for item in extracted_data.line_items
            ],
            "purchase_order": extracted_data.purchase_order.value
            if extracted_data.purchase_order
            else None,
            "vendor_address": extracted_data.vendor_address.value
            if extracted_data.vendor_address
            else None,
            "due_date": extracted_data.due_date.value
            if extracted_data.due_date
            else None,
            "invoice_id": extracted_data.invoice_id.value
            if extracted_data.invoice_id
            else None,
            "notes": extracted_data.notes.value if extracted_data.notes else None,
        }
    elif isinstance(extracted_data, ReceiptExtractionResult):
        raw_data_dict = {
            "document_type": "receipt",
            "merchant_name": extracted_data.merchant_name.value,
            "transaction_date": extracted_data.transaction_date.value,
            "total_amount": extracted_data.total_amount.value,
            "currency": extracted_data.currency.value,
            "tax_amount": extracted_data.tax_amount.value
            if extracted_data.tax_amount
            else None,
            "line_items": [
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price,
                    "currency": item.currency,
                }
                for item in extracted_data.line_items
            ],
            "receipt_id": extracted_data.receipt_id.value
            if extracted_data.receipt_id
            else None,
        }
    else:
        raise ValueError("Unsupported extracted_data type.")

    # Define the target schema as a string for the LLM
    target_schema = NormalizedExpense.schema_json(indent=2)

    prompt = f"""You are an expert in financial document processing. Normalize the following extracted document data into a JSON object strictly adhering to the provided JSON schema. Ensure all dates are in ISO 8601 format (YYYY-MM-DD). If a field is missing or cannot be confidently determined, omit it or set it to null according to the schema. Do not include any additional text or explanations, just the JSON object.

Extracted Document Data ({document_type}):
{json.dumps(raw_data_dict, indent=2)}

Target JSON Schema:
{target_schema}

Normalized JSON:
"""
    # Use the model to generate the normalized JSON
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.0,
            "top_p": 1.0,
            "top_k": 0,
            "response_mime_type": "application/json",
        },
    )

    normalized_json = json.loads(response.text)

    # Post-process to ensure correct types and fill in missing fields from raw_data_dict if LLM misses
    # This also helps to ensure that fields like 'document_type' are correctly set based on input
    final_normalized_data = NormalizedExpense(
        document_type=document_type,
        vendor_name=normalized_json.get("vendor_name")
        or raw_data_dict.get("vendor_name", "UNKNOWN"),
        transaction_date=normalized_json.get("transaction_date")
        or raw_data_dict.get("invoice_date")
        or raw_data_dict.get("transaction_date")
        or datetime.date.today().isoformat(),
        total_amount=float(
            normalized_json.get("total_amount")
            or raw_data_dict.get("total_amount", 0.0)
        ),
        currency=normalized_json.get("currency")
        or raw_data_dict.get("currency", "USD"),
        tax_amount=float(normalized_json["tax_amount"])
        if "tax_amount" in normalized_json and normalized_json["tax_amount"] is not None
        else (
            float(raw_data_dict["tax_amount"])
            if raw_data_dict.get("tax_amount")
            else None
        ),
        line_items=normalized_json.get("line_items", [])
        or raw_data_dict.get("line_items", []),
        notes=normalized_json.get("notes") or raw_data_dict.get("notes"),
        original_document_id=original_document_id,
        extracted_fields=raw_data_dict,
    )

    return final_normalized_data
