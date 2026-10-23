"""
extract_receipt_fields.py

Extracts merchant, tax, total, and items from a receipt using Google Document AI Expense Parser.
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime

from document_client import get_documentai_client, process_document
from document_models import LineItem

def extract_receipt_fields(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str = "application/pdf",
) -> Dict[str, Any]:
    """
    Extracts receipt fields using Google Document AI's Expense Parser.
    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., 'us').
        processor_id: The ID of the Expense Parser processor.
        file_content: The content of the receipt file as bytes.
        mime_type: The MIME type of the file (e.g., 'application/pdf', 'image/jpeg').

    Returns:
        A dictionary containing the extracted receipt fields.
    """
    client = get_documentai_client()
    document = process_document(client, project_id, location, processor_id, file_content, mime_type)

    merchant_name: Optional[str] = None
    transaction_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: list[LineItem] = []
    notes: Optional[str] = None

    for entity in document.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type == "transaction_date":
            try:
                transaction_date = datetime.strptime(entity.mention_text, "%Y-%m-%d").date()
            except ValueError:
                try:
                    transaction_date = datetime.strptime(entity.mention_text, "%m/%d/%Y").date()
                except ValueError:
                    pass
        elif entity.type == "total_amount":
            if entity.money_value:
                total_amount = entity.money_value.amount
                currency = entity.money_value.currency
            elif entity.mention_text:
                try:
                    total_amount = float(entity.mention_text)
                except ValueError:
                    pass
        elif entity.type == "total_tax_amount":
            if entity.money_value:
                tax_amount = entity.money_value.amount
            elif entity.mention_text:
                try:
                    tax_amount = float(entity.mention_text)
                except ValueError:
                    pass
        elif entity.type == "line_item":
            item_description = None
            item_quantity = None
            item_unit_price = None
            item_amount = None
            for prop in entity.properties:
                if prop.type == "description":
                    item_description = prop.mention_text
                elif prop.type == "quantity":
                    try:
                        item_quantity = float(prop.mention_text)
                    except ValueError:
                        pass
                elif prop.type == "unit_price":
                    if prop.money_value:
                        item_unit_price = prop.money_value.amount
                    elif prop.mention_text:
                        try:
                            item_unit_price = float(prop.mention_text)
                        except ValueError:
                            pass
                elif prop.type == "amount":
                    if prop.money_value:
                        item_amount = prop.money_value.amount
                    elif prop.mention_text:
                        try:
                            item_amount = float(prop.mention_text)
                        except ValueError:
                            pass
            line_items.append(LineItem(description=item_description, quantity=item_quantity,
                                       unit_price=item_unit_price, amount=item_amount))
        elif entity.type == "notes": # Example for other potential text fields
            if entity.mention_text:
                if notes:
                    notes += "\n" + entity.mention_text
                else:
                    notes = entity.mention_text

    return {
        "merchant_name": merchant_name,
        "transaction_date": transaction_date,
        "total_amount": total_amount,
        "currency": currency,
        "tax_amount": tax_amount,
        "line_items": line_items,
        "notes": notes,
        "raw_document_output": document.text # For debugging/completeness
    }
