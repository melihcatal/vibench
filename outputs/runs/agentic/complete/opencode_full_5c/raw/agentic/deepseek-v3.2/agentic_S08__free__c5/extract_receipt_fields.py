import os
import json
from typing import Dict, List, Any, Optional
from document_client import get_document_client
from document_models import ReceiptExtractionRequest, ReceiptExtractionResponse


def extract_receipt_fields(file_path: str) -> Dict[str, Any]:
    """
    Extract merchant, tax, total, and items from a receipt using Google Document AI.
    """
    from google.cloud import documentai

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.getenv("DOCUMENT_AI_LOCATION", "us")
    processor_id = os.getenv("RECEIPT_PROCESSOR_ID", "your-processor-id")

    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as f:
        file_content = f.read()

    raw_document = documentai.RawDocument(content=file_content, mime_type="image/jpeg")

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_data = {"merchant": None, "tax": None, "total": None, "items": []}

    # Extract merchant information
    for entity in document.entities:
        if entity.type_ == "store_name":
            extracted_data["merchant"] = entity.mention_text
        elif entity.type_ == "total_amount":
            extracted_data["total"] = entity.mention_text
        elif entity.type_ == "tax_amount":
            extracted_data["tax"] = entity.mention_text
        elif entity.type_ == "line_item":
            item_data = {}
            for prop in entity.properties:
                if prop.type_ == "line_item/description":
                    item_data["description"] = prop.mention_text
                elif prop.type_ == "line_item/amount":
                    item_data["amount"] = prop.mention_text
                elif prop.type_ == "line_item/quantity":
                    item_data["quantity"] = prop.mention_text

            if item_data:
                extracted_data["items"].append(item_data)

    return extracted_data


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        result = extract_receipt_fields(sys.argv[1])
        print(json.dumps(result, indent=2, default=str))
