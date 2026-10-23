import os
from mindee import InvoiceParser


def extract_fields(image_path):
    parser = InvoiceParser(os.getenv("MINDEE_API_KEY"))
    result = parser.parse(image_path)
    return result.dict()
