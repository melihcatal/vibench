def normalize_payload(payload):
    return {'text': payload}


def normalize_response(response):
    return {'embedding': list(response.embeddings[0].values)}