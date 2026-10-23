import os


def normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()


def normalize_text_list(values):
    if values is None:
        return []
    return [normalize_text(v) for v in values if normalize_text(v)]


def build_message_payload(text, metadata=None):
    payload = {"text": normalize_text(text)}
    if metadata:
        payload["metadata"] = dict(metadata)
    return payload


def build_batch_payload(messages):
    return {"messages": [build_message_payload(m) for m in normalize_text_list(messages)]}


def parse_decision(response):
    if isinstance(response, dict):
        return response.get("decision") or response.get("label") or response.get("action")
    return None


def parse_spans(response):
    if isinstance(response, dict):
        spans = response.get("spans") or response.get("redactions") or []
        return spans if isinstance(spans, list) else []
    return []


def get_env(name, default=""):
    return os.getenv(name, default)
