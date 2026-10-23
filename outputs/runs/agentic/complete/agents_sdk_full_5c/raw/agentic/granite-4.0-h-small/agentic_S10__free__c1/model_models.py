import json

def json_schema_to_string(schema: dict) -> str:
    """Convert a JSON Schema dict to a compact string representation suitable for a prompt."""
    return json.dumps(schema, indent=2)

def parse_and_validate_json(raw_text: str, schema: dict) -> dict:
    """
    Try to parse raw_text as JSON; if parsing fails or validation fails,
    raise a helpful exception. Otherwise return the parsed dict.
    """
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Response is not valid JSON: {exc}")

    # Simple validation – ensure the data matches the schema shape (recursive check omitted for brevity)
    missing = [k for k, v in schema.items() if k not in data]
    if missing:
        raise ValueError(f"Missing required keys in JSON output: {', '.join(missing)}")
    return data
