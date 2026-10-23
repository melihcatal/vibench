import os
from typing import List
from mindee import Client, product
from document_models import ExtractedField


def extract_invoice_fields(file_path: str) -> List[ExtractedField]:
    mindee_api_key = os.getenv("MINDEE_API_KEY")
    if not mindee_api_key:
        raise ValueError("MINDEE_API_KEY environment variable is not set")

    mindee_client = Client(api_key=mindee_api_key)
    input_doc = mindee_client.source_from_path(file_path)

    result = mindee_client.parse(product.InvoiceV4, input_doc)

    extracted_fields = []
    if result.document.inference.prediction:
        prediction = result.document.inference.prediction

        for field_name in ["total_amount", "invoice_date", "supplier_name"]:
            field_value = getattr(prediction, field_name)
            if field_value:
                extracted_fields.append(
                    ExtractedField(
                        name=field_name,
                        value=str(field_value.value)
                        if field_value.value is not None
                        else None,
                        confidence=field_value.confidence,
                    )
                )

    return extracted_fields
