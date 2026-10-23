def normalize_embedding(embedding):
    from numpy.linalg import norm
    return embedding / norm(embedding)

def format_request(text):
    return {'instances': [text]}

def parse_response(response):
    return [pred['embedding'] for pred in response.predictions]