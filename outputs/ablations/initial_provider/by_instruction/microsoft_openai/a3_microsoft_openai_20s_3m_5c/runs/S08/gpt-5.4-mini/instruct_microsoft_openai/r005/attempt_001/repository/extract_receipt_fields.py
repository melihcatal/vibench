from document_client import create_client, load_config, extract_json_schema_response


SCHEMA = {
    "type": "object",
    "properties": {
        "merchant": {"type": "string"},
        "tax": {"type": "number"},
        "total": {"type": "number"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "quantity": {"type": "number"},
                    "amount": {"type": "number"},
                },
                "required": ["name", "quantity", "amount"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["merchant", "tax", "total", "items"],
    "additionalProperties": False,
}


def extract_receipt_fields(document_text: str):
    config = load_config()
    client = create_client(config)
    prompt = "Extract receipt merchant, tax, total, and items as JSON." + "\n\n" + document_text
    return extract_json_schema_response(client, config.model, prompt, SCHEMA)
