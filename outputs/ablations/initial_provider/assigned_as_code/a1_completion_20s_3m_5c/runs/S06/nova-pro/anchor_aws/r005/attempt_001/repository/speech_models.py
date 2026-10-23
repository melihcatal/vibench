def normalize_text_payload(payload):
    return {"text": payload["text"], "text_type": "text"}


def normalize_ssml_payload(payload):
    return {"text": payload["ssml"], "text_type": "ssml"}