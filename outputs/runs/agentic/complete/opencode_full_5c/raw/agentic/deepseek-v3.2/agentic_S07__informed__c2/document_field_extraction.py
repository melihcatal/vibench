import os
from typing import Dict, Any, List
from document_client import DocumentClient


def extract_invoice_fields(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extract structured fields from invoice documents using Amazon Textract AnalyzeExpense.

    Args:
        image_bytes: Bytes of the invoice document image

    Returns:
        Structured invoice fields
    """
    # Initialize Textract client
    client = DocumentClient()

    # Call Textract AnalyzeExpense API
    response = client.analyze_expense(image_bytes)

    # Parse expense documents
    expenses = response.get("ExpenseDocuments", [])

    extracted_fields = []

    for expense in expenses:
        expense_fields = {}

        # Extract summary fields
        summary_fields = expense.get("SummaryFields", [])
        for field in summary_fields:
            field_type = field.get("Type", {}).get("Text", "Unknown")
            field_text = ""

            # Get field value text
            for detection in field.get("ValueDetection", {}).get("Text", ""):
                field_text = detection

            # Try to get from Text property
            if not field_text:
                field_text = field.get("ValueDetection", {}).get("Text", "")

            if field_text:
                expense_fields[field_type] = {
                    "value": field_text,
                    "confidence": field.get("Confidence", 0.0),
                }

        # Extract line item groups
        line_item_groups = expense.get("LineItemGroups", [])
        line_items = []

        for group in line_item_groups:
            for line_item in group.get("LineItems", []):
                item_fields = {}

                for field in line_item.get("LineItemExpenseFields", []):
                    field_type = field.get("Type", {}).get("Text", "Unknown")
                    field_text = field.get("ValueDetection", {}).get("Text", "")

                    if field_text:
                        item_fields[field_type] = {
                            "value": field_text,
                            "confidence": field.get("Confidence", 0.0),
                        }

                if item_fields:
                    line_items.append(item_fields)

        extracted_fields.append(
            {
                "summary_fields": expense_fields,
                "line_items": line_items,
                "confidence": expense.get("Confidence", 0.0),
            }
        )

    return {
        "invoice_fields": extracted_fields,
        "total_invoices": len(expenses),
        "provider": "Amazon Textract AnalyzeExpense",
    }


def extract_receipt_fields(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extract structured fields from receipt documents.

    Args:
        image_bytes: Bytes of the receipt document image

    Returns:
        Structured receipt fields
    """
    client = DocumentClient()

    # For receipts, we can use AnalyzeDocument with specific features
    response = client.analyze_document(
        document_bytes=image_bytes, feature_types=["FORMS", "TABLES"]
    )

    blocks = response.get("Blocks", [])

    # Common receipt fields to look for
    receipt_fields = {
        "vendor": None,
        "date": None,
        "total": None,
        "tax": None,
        "items": [],
    }

    # Look for key-value pairs that might be receipt fields
    key_blocks = [
        b
        for b in blocks
        if b.get("BlockType") == "KEY_VALUE_SET" and "KEY" in b.get("EntityTypes", [])
    ]

    for key_block in key_blocks:
        key_text = ""
        value_text = ""

        # Extract key text
        for rel in key_block.get("Relationships", []):
            if rel.get("Type") == "CHILD":
                word_ids = rel.get("Ids", [])
                words = [
                    b
                    for b in blocks
                    if b.get("Id") in word_ids and b.get("BlockType") == "WORD"
                ]
                key_text = " ".join([w.get("Text", "") for w in words]).lower()

        # Find associated value
        for rel in key_block.get("Relationships", []):
            if rel.get("Type") == "VALUE":
                value_ids = rel.get("Ids", [])
                for value_id in value_ids:
                    value_block = next(
                        (b for b in blocks if b.get("Id") == value_id), None
                    )
                    if value_block and "VALUE" in value_block.get("EntityTypes", []):
                        for v_rel in value_block.get("Relationships", []):
                            if v_rel.get("Type") == "CHILD":
                                v_word_ids = v_rel.get("Ids", [])
                                v_words = [
                                    b
                                    for b in blocks
                                    if b.get("Id") in v_word_ids
                                    and b.get("BlockType") == "WORD"
                                ]
                                value_text = " ".join(
                                    [w.get("Text", "") for w in v_words]
                                )

        # Map common receipt fields
        if "vendor" in key_text or "store" in key_text or "merchant" in key_text:
            receipt_fields["vendor"] = {
                "value": value_text,
                "confidence": key_block.get("Confidence", 0.0),
            }
        elif "date" in key_text or "time" in key_text:
            receipt_fields["date"] = {
                "value": value_text,
                "confidence": key_block.get("Confidence", 0.0),
            }
        elif "total" in key_text or "amount" in key_text:
            receipt_fields["total"] = {
                "value": value_text,
                "confidence": key_block.get("Confidence", 0.0),
            }
        elif "tax" in key_text:
            receipt_fields["tax"] = {
                "value": value_text,
                "confidence": key_block.get("Confidence", 0.0),
            }

    return {"receipt_fields": receipt_fields, "provider": "Amazon Textract"}
