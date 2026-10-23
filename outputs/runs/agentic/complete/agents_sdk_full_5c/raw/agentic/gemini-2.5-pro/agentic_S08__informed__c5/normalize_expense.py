"""
Normalizes extracted expense fields into a standard JSON schema using Google Document AI.
"""
import os
import uuid
from google.cloud import documentai

from document_client import get_google_document_ai_client
from document_models import NormalizedExpense, LineItem

def normalize_document_expense(
    file_path: str, mime_type: str, project_id: str, location: str, processor_id: str
) -> NormalizedExpense:
    """
    Processes a document with a Google Document AI processor and normalizes the output.
    """
    docai_client = get_google_document_ai_client()

    with open(file_path, "rb") as image:
        image_content = image.read()

    # The full resource name of the processor
    name = docai_client.processor_path(project_id, location, processor_id)

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
    )

    result = docai_client.process_document(request=request)
    document = result.document

    # Using 'form_parser' processor for generic key-value extraction
    vendor = None
    date = None
    total = None

    for entity in document.entities:
        if entity.type_ == "supplier_name":
            vendor = entity.mention_text
        elif entity.type_ == "invoice_date":
            date = entity.mention_text
        elif entity.type_ == "total_amount":
            try:
                total = float(entity.mention_text.replace("$", "").replace(",", ""))
            except (ValueError, AttributeError):
                total = 0.0

    return NormalizedExpense(
        expense_id=str(uuid.uuid4()),
        vendor=vendor,
        transaction_date=date,
        total_amount=total,
        currency="USD", # Assuming USD from context
        raw_extraction_data={"gcp_docai_entities": [
            {"type": e.type_, "text": e.mention_text} for e in document.entities
        ]}
    )
