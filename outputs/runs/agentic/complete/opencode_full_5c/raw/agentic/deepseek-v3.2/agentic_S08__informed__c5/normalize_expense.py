import json
from typing import Dict, Any
from datetime import datetime
from document_models import DocumentExtraction, parse_textract_expense_response


def normalize_expense(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize extracted expense fields into a standard JSON schema.

    Args:
        extracted_data: Raw extracted data from document extraction service

    Returns:
        Normalized expense record in standard JSON schema
    """
    # Check if this is a Textract response
    if "ExpenseDocuments" in extracted_data:
        # Parse Textract response
        extraction = parse_textract_expense_response(extracted_data)
        normalized = extraction.to_normalized_json()
    else:
        # Assume it's already parsed data from our extractors
        normalized = {
            "vendor": {
                "field_type": "vendor",
                "value": extracted_data.get("vendor"),
                "confidence": extracted_data.get("vendor_confidence", 0.0),
                "label": "Vendor Name",
            }
            if extracted_data.get("vendor")
            else None,
            "merchant": {
                "field_type": "merchant",
                "value": extracted_data.get("merchant"),
                "confidence": extracted_data.get("merchant_confidence", 0.0),
                "label": "Merchant Name",
            }
            if extracted_data.get("merchant")
            else None,
            "date": {
                "field_type": "date",
                "value": extracted_data.get("date"),
                "confidence": extracted_data.get("date_confidence", 0.0),
                "label": "Transaction Date",
            }
            if extracted_data.get("date")
            else None,
            "total": {
                "field_type": "total",
                "value": extracted_data.get("total"),
                "confidence": extracted_data.get("total_confidence", 0.0),
                "label": "Total Amount",
            }
            if extracted_data.get("total")
            else None,
            "tax": {
                "field_type": "tax",
                "value": extracted_data.get("tax"),
                "confidence": extracted_data.get("tax_confidence", 0.0),
                "label": "Tax Amount",
            }
            if extracted_data.get("tax")
            else None,
            "line_items": [],
        }

        # Add line items
        items_key = "line_items" if "line_items" in extracted_data else "items"
        if items_key in extracted_data:
            for item in extracted_data[items_key]:
                normalized_item = {
                    "description": item.get("description", ""),
                    "quantity": item.get("quantity"),
                    "unit_price": item.get("unit_price"),
                    "total_price": item.get("total_price"),
                    "confidence": item.get("confidence", 0.9),
                }
                normalized["line_items"].append(normalized_item)

    # Add metadata
    normalized["normalization_timestamp"] = datetime.utcnow().isoformat()
    normalized["schema_version"] = "1.0"
    normalized["normalization_provider"] = "Amazon Textract AnalyzeExpense"

    # Clean up None values
    normalized = {k: v for k, v in normalized.items() if v is not None}

    return normalized
