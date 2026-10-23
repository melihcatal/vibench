from typing import Dict, List, Optional, TypedDict
import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


class ReceiptItem(TypedDict):
    name: str
    price: float
    quantity: Optional[float]


class ReceiptFields(TypedDict):
    merchant: str
    tax: float
    total: float
    items: List[ReceiptItem]
    confidence: float


def extract_receipt_fields(
    file_path: str, mime_type: str = "image/jpeg"
) -> ReceiptFields:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_DOCUMENT_AI_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_CLOUD_RECEIPT_PROCESSOR_ID")
    processor_version = os.getenv(
        "GOOGLE_CLOUD_RECEIPT_PROCESSOR_VERSION", "pretrained-receipt-v1.2-2023-11-17"
    )

    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    processor_name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    with open(file_path, "rb") as file:
        document_content = file.read()

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=documentai.RawDocument(
            content=document_content, mime_type=mime_type
        ),
    )
    result = client.process_document(request=request)
    document = result.document

    fields = {
        "merchant": "",
        "tax": 0.0,
        "total": 0.0,
        "items": [],
        "confidence": document.confidence,
    }

    for entity in document.entities:
        if entity.type_ == "merchant_name":
            fields["merchant"] = entity.mention_text
        elif entity.type_ == "total_tax":
            fields["tax"] = float(entity.mention_text)
        elif entity.type_ == "total_amount":
            fields["total"] = float(entity.mention_text)
        elif entity.type_ == "line_item":
            item = {
                "name": "",
                "price": 0.0,
                "quantity": None,
            }
            for property_ in entity.properties:
                if property_.type_ == "description":
                    item["name"] = property_.mention_text
                elif property_.type_ == "price":
                    item["price"] = (
                        float(property_.mention_text) if property_.mention_text else 0.0
                    )
                elif property_.type_ == "quantity":
                    item["quantity"] = (
                        float(property_.mention_text)
                        if property_.mention_text
                        else None
                    )
            fields["items"].append(item)

    return fields
