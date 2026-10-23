import json


def normalize_json_secret(value):
    if isinstance(value, str):
        return json.loads(value)
    return value


def rotation_request(payload):
    return {
        "secret_id": payload.get("secret_id") or payload.get("secret_name"),
        "version_id": payload.get("version_id"),
        "version_stage": payload.get("version_stage"),
    }


def text_flagged(value):
    return any(token in (value or "").lower() for token in ("password", "secret", "private", "token"))
