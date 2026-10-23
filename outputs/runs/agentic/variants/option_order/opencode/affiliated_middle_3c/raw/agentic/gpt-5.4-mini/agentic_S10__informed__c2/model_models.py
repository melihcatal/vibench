import json


def normalize_text(text: str) -> str:
    return text.strip()


def safety_result(ok: bool, data):
    return {'ok': ok, 'data': data}


def normalize_json(text: str):
    return json.loads(text)
