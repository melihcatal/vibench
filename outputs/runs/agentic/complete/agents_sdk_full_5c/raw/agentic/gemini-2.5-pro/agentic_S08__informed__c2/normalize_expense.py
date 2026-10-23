
from azure.ai.documentintelligence.models import AnalyzeResult, Document
from document_models import NormalizedExpense, LineItem
from typing import Optional

def _get_field_value(doc: Document, field_name: str, field_type: str):
    field = doc.fields.get(field_name)
    if field and field.type == field_type:
        return field.value
    return None

def normalize_expense(result: AnalyzeResult) -> Optional[NormalizedExpense]:
    """
    Normalizes the result from Azure Document Intelligence into a standard schema.
    """
    if not result.documents or len(result.documents) == 0:
        return None

    doc = result.documents[0]
    
    if doc.doc_type == "prebuilt:invoice":
        items = []
        invoice_items_field = doc.fields.get("Items")
        if invoice_items_field and invoice_items_field.type == "list":
            for item_field in invoice_items_field.value:
                if item_field.type == "dictionary":
                    description = _get_field_value(item_field.value, "Description", "string")
                    quantity = _get_field_value(item_field.value, "Quantity", "number")
                    unit_price = _get_field_value(item_field.value, "UnitPrice", "currency")
                    total_amount = _get_field_value(item_field.value, "Amount", "currency")
                    items.append(LineItem(
                        description=description,
                        quantity=quantity,
                        unit_price=unit_price.amount if unit_price else None,
                        total_amount=total_amount.amount if total_amount else None
                    ))
        
        total_field = doc.fields.get("InvoiceTotal")
        
        return NormalizedExpense(
            vendor_name=_get_field_value(doc, "VendorName", "string"),
            invoice_id=_get_field_value(doc, "InvoiceId", "string"),
            invoice_date=_get_field_value(doc, "InvoiceDate", "date"),
            due_date=_get_field_value(doc, "DueDate", "date"),
            invoice_total=total_field.value.amount if total_field and total_field.type == "currency" else None,
            currency_symbol=total_field.value.symbol if total_field and total_field.type == "currency" else None,
            line_items=items,
            raw_text=result.content,
        )

    elif doc.doc_type == "prebuilt:receipt":
        # Simplified normalization for receipts
        return NormalizedExpense(
            merchant_name=_get_field_value(doc, "MerchantName", "string"),
            transaction_date=_get_field_value(doc, "TransactionDate", "date"),
            tax=_get_field_value(doc, "TotalTax", "currency"),
            total=_get_field_value(doc, "Total", "currency"),
            raw_text=result.content
        )
        
    return None
