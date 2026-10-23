import os
from typing import Dict, List, Any
from google.cloud import documentai
from document_client import get_documentai_client


def validate_document_fields(file_path, document_type):
    client = get_documentai_client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("DOCUMENTAI_LOCATION", "us")

    if document_type == "invoice":
        processor_id = os.environ.get(
            "DOCUMENTAI_INVOICE_PROCESSOR_ID", "invoice-processor"
        )
    elif document_type == "receipt":
        processor_id = os.environ.get(
            "DOCUMENTAI_RECEIPT_PROCESSOR_ID", "receipt-processor"
        )
    else:
        raise ValueError(f"Unsupported document type: {document_type}")

    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    with open(file_path, "rb") as file:
        file_content = file.read()

    mime_type = "application/pdf" if document_type == "invoice" else "image/jpeg"

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    validation_results = {
        "required_fields": [],
        "confidence_scores": {},
        "is_valid": True,
        "missing_fields": [],
    }

    required_field_types = []
    if document_type == "invoice":
        required_field_types = ["supplier_name", "invoice_date", "total_amount"]
    elif document_type == "receipt":
        required_field_types = ["merchant_name", "total_amount"]

    found_fields = set()

    for entity in document.entities:
        field_type = entity.type_
        if field_type in required_field_types:
            found_fields.add(field_type)
            validation_results["confidence_scores"][field_type] = entity.confidence

            validation_results["required_fields"].append(
                {
                    "field": field_type,
                    "value": entity.mention_text,
                    "confidence": entity.confidence,
                    "is_present": True,
                }
            )

    missing_fields = set(required_field_types) - found_fields
    if missing_fields:
        validation_results["is_valid"] = False
        validation_results["missing_fields"] = list(missing_fields)

        for missing_field in missing_fields:
            validation_results["required_fields"].append(
                {
                    "field": missing_field,
                    "value": "",
                    "confidence": 0.0,
                    "is_present": False,
                }
            )

    return validation_results
