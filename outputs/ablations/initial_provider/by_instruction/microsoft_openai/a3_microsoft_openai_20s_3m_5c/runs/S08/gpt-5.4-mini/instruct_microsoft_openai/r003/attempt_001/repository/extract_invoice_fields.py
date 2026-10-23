from document_client import chat_json


def extract_invoice_fields(document_text: str):
    return chat_json(
        document_text,
        {
            "vendor": "string",
            "date": "string",
            "total": "number",
            "line_items": [{"description": "string", "quantity": "number", "amount": "number"}],
        },
    )
