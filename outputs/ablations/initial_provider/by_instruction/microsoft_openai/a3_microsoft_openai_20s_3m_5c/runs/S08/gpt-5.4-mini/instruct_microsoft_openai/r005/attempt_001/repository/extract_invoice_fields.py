from document_client import create_client, load_config, extract_json_schema_response


SCHEMA = {
    "type": "object",
    "properties": {
        "vendor": {"type": "string"},
        "date": {"type": "string"},
        "total": {"type": "number"},
        "line_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "quantity": {"type": "number"},
                    "unit_price": {"type": "number"},
                    "amount": {"type": "number"},
                },
                "required": ["description", "quantity", "unit_price", "amount"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["vendor", "date", "total", "line_items"],
    "additionalProperties": False,
}


def extract_invoice_fields(document_text: str):
    config = load_config()
    client = create_client(config)
    prompt = "Extract invoice vendor, date, total, and line-item fields as JSON." + "\n\n" + document_text
    return extract_json_schema_response(client, config.model, prompt, SCHEMA)
