def normalize_document_response(response):
    normalized_response = {
        "expense_documents": [
            {
                "vendor_name": doc["SummaryFields"][0].get("ValueDetection", {}).get("Text", ""),
                "total": doc["SummaryFields"][1].get("ValueDetection", {}).get("Text", ""),
                "line_items": [
                    {
                        "description": item["LineItemExpenseFields"][0].get("ValueDetection", {}).get("Text", ""),
                        "quantity": item["LineItemExpenseFields"][1].get("ValueDetection", {}).get("Text", ""),
                        "amount": item["LineItemExpenseFields"][2].get("ValueDetection", {}).get("Text", "")
                    }
                    for item in doc["LineItemGroups"][0].get("LineItems", [])
                ]
            }
            for doc in response["ExpenseDocuments"]
        ]
    }
    return normalized_response