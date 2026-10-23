import json


def normalize_text(value) -> str:
    return "" if value is None else str(value).strip()


def summarize_result(response) -> str:
    return response.choices[0].message.content.strip()


def parse_json_response(response) -> dict:
    content = response.choices[0].message.content
    return json.loads(content)
