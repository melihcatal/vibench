def normalize_embedding(embedding):
    return [float(f) for f in embedding]


def parse_response(response):
    return response["data"][0]["embedding"]
