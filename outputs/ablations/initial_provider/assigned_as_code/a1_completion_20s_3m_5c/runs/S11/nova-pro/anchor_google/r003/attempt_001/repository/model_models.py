def normalize_payload(payload):
    return {"text": payload["text"]}


def normalize_response(response):
    return {"text": response.text or ""}