from typing import Dict, List, Optional, TypedDict
import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


class LineItem(TypedDict):
    description: str
    quantity: float
    unit_price: float
    amount: float


class InvoiceFields(TypedDict):
    vendor: str
    date: str
    total: float
    line_items: List[LineItem]
    confidence: float


def extract_invoice_fields(
    file_path: str, mime_type: str = "application/pdf"
) -> InvoiceFields:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_DOCUMENT_AI_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_CLOUD_INVOICE_PROCESSOR_ID")
    processor_version = os.getenv(
        "GOOGLE_CLOUD_INVOICE_PROCESSOR_VERSION", "pretrained-invoice-v1.2-2023-11-17"
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
        "vendor": "",
        "date": "",
        "total": 0.0,
        "line_items": [],
        "confidence": document.confidence,
    }

    for entity in document.entities:
        if entity.type_ == "supplier_name":
            fields["vendor"] = entity.mention_text
        elif entity.type_ == "invoice_date":
            fields["date"] = entity.mention_text
        elif entity.type_ == "total_amount":
            fields["total"] = float(entity.mention_text)
        elif entity.type_ == "line_item":
            line_item = {
                "description": "",
                "quantity": 0.0,
                "unit_price": 0.0,
                "amount": 0.0,
            }
            for property_ in entity.properties:
                if property_.type_ == "description":
                    line_item["description"] = property_.mention_text
                elif property_.type_ == "quantity":
                    line_item["quantity"] = (
                        float(property_.mention_text) if property_.mention_text else 0.0
                    )
                elif property_.type_ == "unit_price":
                    line_item["unit_price"] = (
                        float(property_.mention_text) if property_.mention_text else 0.0
                    )
                elif property_.type_ == "amount":
                    line_item["amount"] = (
                        float(property_.mention_text) if property_.mention_text else 0.0
                    )
            fields["line_items"].append(line_item)

    return fields
