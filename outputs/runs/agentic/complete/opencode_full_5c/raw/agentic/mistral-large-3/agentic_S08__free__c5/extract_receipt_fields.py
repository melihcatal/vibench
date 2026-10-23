from typing import Dict, Any, Optional
import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


def extract_receipt_fields(
    file_path: str, mime_type: str = "image/jpeg"
) -> Dict[str, Any]:
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_DOCUMENT_AI_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_CLOUD_RECEIPT_PROCESSOR_ID")
    processor_version = os.getenv(
        "GOOGLE_CLOUD_RECEIPT_PROCESSOR_VERSION", "pretrained-receipt-v1.0-2023-11-17"
    )

    if not all([project_id, processor_id]):
        raise ValueError(
            "Missing required Google Cloud Document AI environment variables."
        )

    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)
    processor_name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    with open(file_path, "rb") as file:
        document = {"content": file.read(), "mime_type": mime_type}

    request = documentai.ProcessRequest(name=processor_name, raw_document=document)
    result = client.process_document(request=request)
    document = result.document

    extracted_fields = {
        "merchant": None,
        "tax": None,
        "total": None,
        "items": [],
        "confidence": document.confidence,
    }

    for entity in document.entities:
        if entity.type_ == "merchant_name":
            extracted_fields["merchant"] = entity.mention_text
        elif entity.type_ == "total_tax":
            extracted_fields["tax"] = float(entity.mention_text)
        elif entity.type_ == "total_amount":
            extracted_fields["total"] = float(entity.mention_text)
        elif entity.type_ == "line_item":
            item = {"description": None, "quantity": None, "price": None}
            for prop in entity.properties:
                if prop.type_ == "line_item_description":
                    item["description"] = prop.mention_text
                elif prop.type_ == "line_item_quantity":
                    item["quantity"] = float(prop.mention_text)
                elif prop.type_ == "line_item_price":
                    item["price"] = float(prop.mention_text)
            if any(item.values()):
                extracted_fields["items"].append(item)

    return extracted_fields
