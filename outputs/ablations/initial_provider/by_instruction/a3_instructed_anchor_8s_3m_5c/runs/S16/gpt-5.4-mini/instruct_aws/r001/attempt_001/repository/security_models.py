import json


def normalize_secret_text(secret_text: str) -> str:
    return secret_text.strip()


def parse_json_secret(secret_text: str):
    return json.loads(secret_text)


def secret_version_request(secret_id: str, version_stage: str | None = None, version_id: str | None = None) -> dict:
    data = {"secret_id": secret_id}
    if version_stage:
        data["version_stage"] = version_stage
    if version_id:
        data["version_id"] = version_id
    return data


def summarize_rotation(version_id: str | None, version_stage: str | None, rotated: bool) -> dict:
    return {"version_id": version_id, "version_stage": version_stage, "rotated": rotated}
