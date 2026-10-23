from typing import Any, Dict, Optional
from document_models import ExpenseDocument, LineItem
from azure.ai.documentintelligence.models import AnalyzeResult


def normalize_extracted_data(
    raw_extraction_data: Dict[str, Any], document_type: str = "invoice"
) -> ExpenseDocument:
    normalized_expense = ExpenseDocument(
        raw_extraction_data=raw_extraction_data, document_type=document_type
    )

    if document_type == "invoice":
        if "documents" in raw_extraction_data and raw_extraction_data["documents"]:
            invoice_fields = raw_extraction_data["documents"][0].get("fields", {})

            normalized_expense.vendor_name = invoice_fields.get("VendorName", {}).get(
                "valueString"
            )
            normalized_expense.document_date = invoice_fields.get(
                "InvoiceDate", {}
            ).get("valueDate")
            normalized_expense.total_amount = invoice_fields.get(
                "InvoiceTotal", {}
            ).get("valueNumber")
            normalized_expense.currency = invoice_fields.get("InvoiceTotal", {}).get(
                "currencySymbol"
            )

            if "Items" in invoice_fields and invoice_fields["Items"].get("valueArray"):
                for item_field in invoice_fields["Items"]["valueArray"]:
                    item_data = item_field.get("valueObject", {})
                    line_item = LineItem(
                        description=item_data.get("Description", {}).get("valueString"),
                        quantity=item_data.get("Quantity", {}).get("valueNumber"),
                        unit_price=item_data.get("UnitPrice", {}).get("valueNumber"),
                        total_price=item_data.get("Amount", {}).get("valueNumber"),
                    )
                    normalized_expense.line_items.append(line_item)
    elif document_type == "receipt":
        if (
            "ExpenseDocuments" in raw_extraction_data
            and raw_extraction_data["ExpenseDocuments"]
        ):
            expense_document = raw_extraction_data["ExpenseDocuments"][0]
            summary_fields = expense_document.get("SummaryFields", [])
            line_item_groups = expense_document.get("LineItemGroups", [])

            for field in summary_fields:
                field_type = field.get("Type", {}).get("Text")
                field_value = field.get("ValueDetection", {}).get("Text")
                if field_type == "TOTAL":
                    normalized_expense.total_amount = (
                        float(field_value) if field_value else None
                    )
                elif field_type == "TAX":
                    normalized_expense.tax_amount = (
                        float(field_value) if field_value else None
                    )
                elif field_type == "VENDOR_NAME":
                    normalized_expense.merchant_name = field_value
                elif field_type == "DATE":
                    normalized_expense.document_date = field_value

            for group in line_item_groups:
                for item_block in group.get("LineItems", []):
                    item_fields = item_block.get("LineItemExpenseFields", [])
                    item_data = {}
                    for item_field in item_fields:
                        item_type = item_field.get("Type", {}).get("Text")
                        item_value = item_field.get("ValueDetection", {}).get("Text")
                        if item_type == "ITEM":
                            item_data["description"] = item_value
                        elif item_type == "PRICE":
                            item_data["total_price"] = (
                                float(item_value) if item_value else None
                            )
                    if item_data:
                        normalized_expense.line_items.append(LineItem(**item_data))

    return normalized_expense
