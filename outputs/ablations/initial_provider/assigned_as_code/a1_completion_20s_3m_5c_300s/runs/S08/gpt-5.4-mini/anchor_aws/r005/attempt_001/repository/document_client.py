import os


def get_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        "table_name": config.get("table_name") or os.environ.get("DYNAMODB_TABLE_NAME"),
        "model_id": config.get("model_id") or os.environ.get("OPENAI_MODEL", "gpt-5.4-mini"),
        "moderation_model": config.get("moderation_model") or os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        "translate_model": config.get("translate_model") or os.environ.get("OPENAI_TRANSLATE_MODEL", "gpt-4o-mini"),
    }


def normalize_document_payload(payload):
    if isinstance(payload, dict):
        return payload
    return {"document_bytes": payload}


def text_from_bytes(payload):
    data = payload.get("document_bytes", b"")
    if isinstance(data, str):
        return data
    return data.decode("utf-8", errors="ignore")
