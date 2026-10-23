def normalize_payload(payload):
    return {'id': {'S': payload['id']}, 'document': {'S': payload['document']}}


def parse_response(response):
    return {k: v[list(v.keys())[0]] for k, v in response.items()}
