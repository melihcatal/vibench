from safety_client import moderate_text_payload, redact_spans


def redact_unsafe(text):
    payload = moderate_text_payload(text)
    return {
        "redacted_text": redact_spans(text, payload["flagged_spans"]),
        "flagged": not payload["allowed"],
        "categories": payload["categories"],
    }
