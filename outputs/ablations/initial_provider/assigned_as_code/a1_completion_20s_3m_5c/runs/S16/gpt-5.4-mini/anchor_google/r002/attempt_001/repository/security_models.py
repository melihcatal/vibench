import json


def get_secret_name(payload, config):
    return payload.get("secret_id") or config.get("secret_id")


def get_version_name(payload, config):
    return payload.get("version") or config.get("version") or "latest"


def normalize_secret_text(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


def parse_json_payload(text):
    return json.loads(normalize_secret_text(text))


def build_secret_path(project_id, secret_id, version):
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
