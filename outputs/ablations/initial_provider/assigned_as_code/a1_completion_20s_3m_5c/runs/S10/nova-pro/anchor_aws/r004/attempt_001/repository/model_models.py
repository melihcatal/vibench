def normalize_payload(payload):
    return {
        "text": payload.get("text", ""),
    }


def normalize_response(response):
    return {
        "text": response.get("text", ""),
    }