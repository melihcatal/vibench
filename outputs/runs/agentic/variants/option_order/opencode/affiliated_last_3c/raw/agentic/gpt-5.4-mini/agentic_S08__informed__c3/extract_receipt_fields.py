from document_client import textract_client


def extract_receipt_fields(document_bytes: bytes) -> dict:
    client = textract_client()
    response = client.analyze_expense(Document={"Bytes": document_bytes})
    result = {"merchant": None, "tax": None, "total": None, "items": []}
    for expense in response.get("ExpenseDocuments", []):
        for field in expense.get("SummaryFields", []):
            t = field.get("Type", {}).get("Text")
            v = field.get("ValueDetection", {}).get("Text")
            if t == "VENDOR_NAME":
                result["merchant"] = v
            elif t == "TOTAL_TAX":
                result["tax"] = v
            elif t == "TOTAL":
                result["total"] = v
        for group in expense.get("LineItemGroups", []):
            for item in group.get("LineItems", []):
                extracted = {}
                for field in item.get("LineItemExpenseFields", []):
                    t = field.get("Type", {}).get("Text")
                    v = field.get("ValueDetection", {}).get("Text")
                    if t:
                        extracted[t.lower()] = v
                if extracted:
                    result["items"].append(extracted)
    return result
