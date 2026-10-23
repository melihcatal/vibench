import os
from typing import List, Dict, Any
from mindee import Client, product
from document_models import StructuredField


def document_field_extraction(file_path: str) -> List[StructuredField]:
    """
    Extracts structured fields from a document (e.g., an invoice) using Mindee.
    """
    mindee_api_key = os.environ.get("MINDEE_API_KEY")
    if not mindee_api_key:
        raise ValueError("MINDEE_API_KEY environment variable not set.")

    mindee_client = Client(api_key=mindee_api_key)
    input_doc = mindee_client.source_from_path(file_path)

    result = mindee_client.parse(product.InvoiceV4, input_doc)

    doc = result.document
    extracted_fields = []

    if doc.inference and doc.inference.prediction:
        prediction = doc.inference.prediction
        fields_to_extract: Dict[str, Any] = {
            "invoice_number": prediction.invoice_number,
            "total_amount": prediction.total_amount,
            "invoice_date": prediction.invoice_date,
            "supplier_name": prediction.supplier_name,
            "customer_name": prediction.customer_name,
        }
        for name, field in fields_to_extract.items():
            if field:
                extracted_fields.append(
                    StructuredField(
                        name=name, value=field.value, confidence=field.confidence
                    )
                )

    return extracted_fields
