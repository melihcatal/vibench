from database_client import load_config


def record_summary(payload, config=None):
    load_config(config)
    record = payload["record"]
    fields = record if isinstance(record, dict) else {}
    return {"id": fields.get("id"), "summary": "; ".join(f"{k}={v}" for k, v in list(fields.items())[:5])}
