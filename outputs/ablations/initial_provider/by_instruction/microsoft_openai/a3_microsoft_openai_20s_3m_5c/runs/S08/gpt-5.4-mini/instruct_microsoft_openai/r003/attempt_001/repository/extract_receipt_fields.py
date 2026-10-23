from document_client import chat_json


def extract_receipt_fields(document_text: str):
    return chat_json(
        document_text,
        {
            "merchant": "string",
            "tax": "number",
            "total": "number",
            "items": [{"name": "string", "price": "number"}],
        },
    )
