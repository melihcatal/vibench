import json

import requests


def normalize_expense(payload, config=None):
    config = config or {}
    endpoint = config.get("endpoint", "https://api.openai.com/v1/responses")
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "expense_normalization",
            "schema": {
                "type": "object",
                "properties": {
                    "vendor": {"type": ["string", "null"]},
                    "date": {"type": ["string", "null"]},
                    "total": {"type": ["string", "number", "null"]},
                    "currency": {"type": ["string", "null"]},
                    "line_items": {"type": "array"},
                },
                "required": ["vendor", "date", "total", "currency", "line_items"],
                "additionalProperties": True,
            },
        },
    }
    response = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"},
        json={
            "model": config.get("model", "gpt-5.4-mini"),
            "input": json.dumps(payload),
            "response_format": schema,
        },
        timeout=config.get("timeout", 60),
    )
    response.raise_for_status()
    return response.json()
