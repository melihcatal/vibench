from pathlib import Path
import json


def build_request_payload(document_type: str, data: dict) -> dict:
    """Construct a request payload for the Structured Document Extraction service.

    Returns a dict ready to be sent to the provider SDK or REST endpoint.
    """
    # Simple schema mapping; real implementation would adapt to each provider's spec
    if document_type == "invoice":
        return {
            "documentType": "invoice",
            "file": Path(data.get("file_path", "")).read_bytes(),
            "options": {
                "vendorField": "vendor",
                "dateField": "date",
                "totalField": "total",
                "lineItemsField": "line_items",
            },
        }
    elif document_type == "receipt":
        return {
            "documentType": "receipt",
            "file": Path(data.get("file_path", "")).read_bytes(),
            "options": {
                "merchantField": "merchant",
                "taxField": "tax",
                "totalField": "total",
                "itemsField": "items",
            },
        }
    else:
        raise ValueError(f"Unsupported document_type: {document_type}")


# Example local helper usage (uncomment to test)
# payload = build_request_payload('invoice', {'file_path': 'path/to/invoice.pdf'})
# print(json.dumps(payload, indent=2))
