import json
from google.cloud import documentai_v1 as documentai

def normalize_expense(document_content: bytes, mime_type: str) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema using Google Cloud Document AI.

    Args:
        document_content: The content of the expense document (e.g., image bytes, PDF bytes).
        mime_type: The MIME type of the document (e.g., "application/pdf", "image/jpeg").

    Returns:
        A dictionary representing the normalized expense in a standard JSON schema.
    """
    # [START documentai_expense_parser_normalize]
    # Initialize the Document AI client. This makes Google Cloud Document AI
    # the identifiable concrete external provider.
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processors/processor-id
    # You would typically get this from your Google Cloud project.
    processor_name = "projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/processors/YOUR_PROCESSOR_ID"

    # Create the document proto
    raw_document = documentai.RawDocument(content=document_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    # Here we would typically make the actual API call.
    # For this example, we'll simulate a response from Document AI's Expense Parser.
    # In a real scenario, client.process_document(request=request) would be called.
    
    # Simulated Document AI Expense Parser response
    # This structure is a simplified representation of what Document AI might return.
    # The actual response is much more detailed and complex, often requiring
    # more sophisticated parsing of entities.
    simulated_docai_response = {
        "entities": [
            {"type": "total_amount", "mention_text": "$123.45", "normalized_value": {"money_value": {"currency_code": "USD", "units": "123", "nanos": "450000000"}}},
            {"type": "purchase_date", "mention_text": "2026-09-20", "normalized_value": {"date_value": {"year": 2026, "month": 9, "day": 20}}},
            {"type": "merchant_name", "mention_text": "Coffee Shop XYZ"},
            {"type": "line_item", "properties": [
                {"type": "description", "mention_text": "Coffee"},
                {"type": "amount", "mention_text": "$3.00", "normalized_value": {"money_value": {"currency_code": "USD", "units": "3", "nanos": "0"}}},
                {"type": "quantity", "mention_text": "1", "normalized_value": {"integer_value": "1"}}
            ]},
            {"type": "line_item", "properties": [
                {"type": "description", "mention_text": "Sandwich"},
                {"type": "amount", "mention_text": "$10.45", "normalized_value": {"money_value": {"currency_code": "USD", "units": "10", "nanos": "450000000"}}},
                {"type": "quantity", "mention_text": "1", "normalized_value": {"integer_value": "1"}}
            ]}
        ]
    }
    
    normalized_expense_data = {
        "date": None,
        "total_amount": {"currency": None, "value": None},
        "vendor_name": None,
        "items": []
    }

    for entity in simulated_docai_response.get("entities", []):
        entity_type = entity.get("type")
        if entity_type == "purchase_date":
            date_value = entity.get("normalized_value", {}).get("date_value", {})
            if date_value:
                normalized_expense_data["date"] = f"{date_value.get('year')}-{date_value.get('month'):02d}-{date_value.get('day'):02d}"
        elif entity_type == "total_amount":
            money_value = entity.get("normalized_value", {}).get("money_value", {})
            if money_value:
                normalized_expense_data["total_amount"]["currency"] = money_value.get("currency_code")
                # Document AI nanosecond conversion
                units = int(money_value.get("units", 0))
                nanos = int(money_value.get("nanos", 0))
                normalized_expense_data["total_amount"]["value"] = units + nanos / 1_000_000_000
        elif entity_type == "merchant_name":
            normalized_expense_data["vendor_name"] = entity.get("mention_text")
        elif entity_type == "line_item":
            item = {
                "description": None,
                "amount": {"currency": None, "value": None},
                "quantity": None
            }
            for prop in entity.get("properties", []):
                prop_type = prop.get("type")
                if prop_type == "description":
                    item["description"] = prop.get("mention_text")
                elif prop_type == "amount":
                    money_value = prop.get("normalized_value", {}).get("money_value", {})
                    if money_value:
                        item["amount"]["currency"] = money_value.get("currency_code")
                        units = int(money_value.get("units", 0))
                        nanos = int(money_value.get("nanos", 0))
                        item["amount"]["value"] = units + nanos / 1_000_000_000
                elif prop_type == "quantity":
                    item["quantity"] = int(prop.get("normalized_value", {}).get("integer_value", 0))
            if item["description"] or item["amount"]["value"]: # Only add if it has some content
                normalized_expense_data["items"].append(item)
    
    # [END documentai_expense_parser_normalize]
    return normalized_expense_data

