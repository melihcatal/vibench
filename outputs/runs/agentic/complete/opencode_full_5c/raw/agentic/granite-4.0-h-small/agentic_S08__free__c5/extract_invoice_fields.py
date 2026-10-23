# provider: Azure Form Recognizer

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_models import InvoiceFieldsResponse

# Local helper import for configuration
from document_client import (
    get_form_recognizer_credentials,
    get_form_recognizer_endpoint,
)

ENDPOINT = get_form_recognizer_endpoint()
KEY = get_form_recognizer_credentials()

client = DocumentAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))
MODEL_ID = "prebuilt-expense"


def extract_invoice_fields(file_path: str) -> InvoiceFieldsResponse:
    poller = client.begin_analyze_document(MODEL_ID, file_path)
    result = poller.result()

    vendor = None
    date_str = None
    total = None
    line_items = []

    for field in result.fields:
        name = field.name.lower()
        value = field.value if field.value else ""
        confidence = field.confidence

        if name == "vendor":
            vendor = value
        elif name == "date posted":
            date_str = value
        elif name == "total":
            total = value
        elif name == "line item details":
            for line in value:
                line_items.append(
                    {
                        "description": line.get("description", "").strip(),
                        "quantity": line.get("quantity", "").strip(),
                        "unit_price": line.get("unit price", "").strip(),
                        "total": line.get("total", "").strip(),
                    }
                )

    return InvoiceFieldsResponse(
        vendor=vendor,
        date=date_str,
        total=total,
        line_items=line_items,
    )


if __name__ == "__main__":
    import sys
    from pprint import pprint

    if len(sys.argv) < 2:
        print("Usage: python extract_invoice_fields.py <path_to_invoice>\n")
        sys.exit(1)

    invoice_file = sys.argv[1]
    result = extract_invoice_fields(invoice_file)
    pprint(result.dict())
