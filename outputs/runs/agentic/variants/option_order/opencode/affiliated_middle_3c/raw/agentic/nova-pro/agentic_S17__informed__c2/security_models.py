from base64 import b64encode, b64decode


def normalize_payload(payload):
    return b64encode(payload).decode("utf-8")


def denormalize_payload(normalized_payload):
    return b64decode(normalized_payload)
