def normalize_payload(payload):
    return payload.encode('utf-8')

def parse_response(response):
    return response.result()