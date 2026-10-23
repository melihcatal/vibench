def normalize_payload(payload):
    return {k: v for k, v in payload.items() if v is not None}

def normalize_response(response):
    return {k: v for k, v in response.items() if v is not None}