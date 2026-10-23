from mindee import Client
from mindee.product import InvoiceV4


def document_field_extraction(file_path: str) -> dict:
    """
    Extract structured fields from OCR-normalized document text.
    Uses Mindee for invoice processing.
    """
    mindee_client = Client()
    input_source = mindee_client.source_from_path(file_path)

    result = mindee_client.parse(InvoiceV4, input_source)

    if result.document:
        return result.document.inference.prediction.to_dict()
    return {}
