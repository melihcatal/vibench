import requests

from identity_models import normalize_audit_record


def audit_summary(payload, config=None):
    config = dict(config or {})
    response = requests.post("https://language.googleapis.com/v1/documents:analyzeSentiment",
                             params={"key": config["api_key"]}, json={"document": {"content": payload["text"], "type": "PLAIN_TEXT"}}, timeout=30)
    response.raise_for_status()
    result = response.json()
    record = normalize_audit_record(payload)
    record["sentiment"] = result.get("documentSentiment", {})
    return record
