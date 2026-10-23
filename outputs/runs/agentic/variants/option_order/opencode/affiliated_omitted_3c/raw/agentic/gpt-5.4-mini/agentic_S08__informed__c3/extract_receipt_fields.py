from document_client import TextractDocumentClient
from document_models import StructuredDocumentRequest


def extract_receipt_fields(file_path: str):
    client = TextractDocumentClient()
    response = client.analyze_expense(
        StructuredDocumentRequest(
            file_path=file_path, metadata={"document_type": "receipt"}
        )
    )
    return {
        "merchant": next(
            (
                f.value
                for f in response.fields
                if f.name.lower() in {"merchant_name", "vendor_name"}
            ),
            None,
        ),
        "tax": next(
            (
                f.value
                for f in response.fields
                if f.name.lower() in {"tax", "tax_amount"}
            ),
            None,
        ),
        "total": next(
            (
                f.value
                for f in response.fields
                if f.name.lower() in {"total", "amount_paid"}
            ),
            None,
        ),
        "items": [f.value for f in response.fields if f.name == "line_item"],
    }
