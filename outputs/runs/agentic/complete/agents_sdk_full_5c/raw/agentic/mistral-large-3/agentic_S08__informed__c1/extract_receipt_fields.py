import os
from typing import Dict, Any
from google.cloud import documentai_v1 as documentai
from document_models import ReceiptFields

client = documentai.DocumentProcessorServiceClient()
processor_name = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_NAME")


def extract_receipt_fields(file_path: str) -> Dict[str, Any]:
    with open(file_path, "rb") as file:
        content = file.read()
    
    request = {
        "name": processor_name,
        "raw_document": {"content": content, "mime_type": "application/pdf"},
    }
    result = client.process_document(request=request)
    document = result.document
    
    fields = document.entities
    
    result = {
        "merchant": next((f.normalized_value.text for f in fields if f.type_ == "merchant_name"), None),
        "tax": next((f.normalized_value.text for f in fields if f.type_ == "total_tax"), None),
        "total": next((f.normalized_value.text for f in fields if f.type_ == "total_amount"), None),
        "items": [
            {
                "description": item.normalized_value.text,
                "price": next(
                    (f.normalized_value.text for f in item.properties if f.type_ == "price"), None
                ),
            }
            for item in fields
            if item.type_ == "line_item"
        ],
        "confidence": document.confidence,
    }
    return result