from document_models import ExpenseRecord, LineItem


def normalize_expense(extracted_data: dict) -> ExpenseRecord:
    document_type = list(extracted_data.keys())[0]
    data = extracted_data[document_type][0]

    if document_type == "invoices":
        return ExpenseRecord(
            document_type="invoice",
            vendor_name=data.get("vendor"),
            transaction_date=data.get("date"),
            total_amount=data.get("total"),
            line_items=[LineItem(**item) for item in data.get("line_items", [])]
        )
    elif document_type == "receipts":
        return ExpenseRecord(
            document_type="receipt",
            merchant_name=data.get("merchant"),
            tax_amount=data.get("tax"),
            total_amount=data.get("total"),
            line_items=[LineItem(**item) for item in data.get("items", [])]
        )
    else:
        raise ValueError(f"Unknown document type: {document_type}")
