def normalize_expense(extracted_data: dict, document_type: str) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    The schema is simplified for this example.
    """
    normalized_record = {
        "document_type": document_type,
        "vendor_name": None,
        "transaction_date": None,
        "total_amount": None,
        "currency": None,
        "line_items": [],
        "raw_extraction": extracted_data # Keep raw data for debugging/audit
    }

    # Example: Simple normalization based on document type (simplified)
    if document_type == "invoice":
        # Placeholder for invoice specific normalization logic
        # E.g., parse from AWS Textract AnalyzeDocument blocks
        pass
    elif document_type == "receipt":
        # Placeholder for receipt specific normalization logic
        # E.g., parse from AWS Textract AnalyzeExpense responses
        if "ExpenseDocuments" in extracted_data and extracted_data["ExpenseDocuments"]:
            expense = extracted_data["ExpenseDocuments"][0]
            if "SummaryFields" in expense:
                for field in expense["SummaryFields"]:
                    if field.get("Type", {}).get("Text") == "VENDOR_NAME":
                        normalized_record["vendor_name"] = field.get("ValueDetection", {}).get("Text")
                    elif field.get("Type", {}).get("Text") == "TOTAL":
                        normalized_record["total_amount"] = float(field.get("ValueDetection", {}).get("Text")) if field.get("ValueDetection", {}).get("Text") else None
                        normalized_record["currency"] = field.get("ValueDetection", {}).get("Currency")
                    elif field.get("Type", {}).get("Text") == "DATE":
                        normalized_record["transaction_date"] = field.get("ValueDetection", {}).get("Text")
            
            if "LineItemGroups" in expense:
                for group in expense["LineItemGroups"]:
                    for item in group.get("LineItems", []):
                        item_data = {}
                        for field in item.get("LineItemFields", []):
                            field_type = field.get("Type", {}).get("Text")
                            field_value = field.get("ValueDetection", {}).get("Text")
                            if field_type == "ITEM":
                                item_data["description"] = field_value
                            elif field_type == "PRICE":
                                item_data["price"] = float(field_value) if field_value else None
                            elif field_type == "QUANTITY":
                                item_data["quantity"] = int(field_value) if field_value else None
                        if item_data: 
                            normalized_record["line_items"].append(item_data)

    return normalized_record
