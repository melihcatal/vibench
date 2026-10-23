def normalize_request(payload):
    return {
        "text": payload["text"]
    }


def normalize_response(response):
    return {
        "text": response.text,
        "usage": response.usage,
        "resource_id": response.resource_id,
        "model_handle": response.model_handle
    }
