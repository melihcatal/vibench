from document_client import TextractDocumentClient
from document_models import StructuredDocumentRequest


def extract_invoice_fields(file_path: str):
    client = TextractDocumentClient()
    response = client.analyze_expense(
        StructuredDocumentRequest(
            file_path=file_path, metadata={"document_type": "invoice"}
        )
    )
    return {
        "vendor": next(
            (
                f.value
                for f in response.fields
                if f.name.lower() in {"vendor_name", "supplier_name"}
            ),
            None,
        ),
        "date": next(
            (
                f.value
                for f in response.fields
                if f.name.lower()
                in {"invoice_receipt_date", "transaction_date", "date"}
            ),
            None,
        ),
        "total": next(
            (
                f.value
                for f in response.fields
                if f.name.lower() in {"total", "amount_due", "amount_paid"}
            ),
            None,
        ),
        "line_items": [f.value for f in response.fields if f.name == "line_item"],
    }
