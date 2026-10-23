def normalize_payload(payload):
    return {
        'id': payload['id'],
        'document': payload['document']
    }


def normalize_response(response):
    return {
        'id': response['id']
    }