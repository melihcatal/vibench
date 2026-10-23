import json


def load_json_secret(secret_text):
    if not secret_text:
        return {}
    if isinstance(secret_text, bytes):
        secret_text = secret_text.decode("utf-8")
    data = json.loads(secret_text)
    return data if isinstance(data, dict) else {"value": data}


def connection_string_from_secret(secret_value):
    if isinstance(secret_value, dict):
        host = secret_value.get("host", "")
        user = secret_value.get("username", "")
        password = secret_value.get("password", "")
        db = secret_value.get("database", "")
        return f"postgresql://{user}:{password}@{host}/{db}"
    return str(secret_value)


def rotation_payload(version_id=None, stage=None):
    payload = {}
    if version_id:
        payload["VersionId"] = version_id
    if stage:
        payload["VersionStage"] = stage
    return payload
