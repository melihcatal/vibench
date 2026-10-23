def normalize_response(response):
    normalized = {}
    for category, score in response.items():
        normalized[category] = score
    return normalized