from document_models import ExpenseRecord, LineItem


def normalize_expense(extracted_data: dict) -> ExpenseRecord:
    document_type = list(extracted_data.keys())[0]
    data = extracted_data[document_type][0]

    if document_type == "invoices":
        line_items = [LineItem(description=item.get("description"), quantity=item.get("quantity"), amount=item.get("amount"))
                      for item in data.get("line_items", [])]
        return ExpenseRecord(
            document_type="invoice",
            vendor_name=data.get("vendor"),
            transaction_date=data.get("date"),
            total_amount=data.get("total"),
            line_items=line_items,
            raw_extraction=extracted_data
        )
    elif document_type == "receipts":
        line_items = [LineItem(description=item.get("description"), quantity=item.get("quantity"), amount=item.get("amount"))
                      for item in data.get("items", [])]
        return ExpenseRecord(
            document_type="receipt",
            vendor_name=data.get("merchant"),
            tax_amount=data.get("tax"),
            total_amount=data.get("total"),
            line_items=line_items,
            raw_extraction=extracted_data
        )
    else:
        raise ValueError(f"Unknown document type: {document_type}")