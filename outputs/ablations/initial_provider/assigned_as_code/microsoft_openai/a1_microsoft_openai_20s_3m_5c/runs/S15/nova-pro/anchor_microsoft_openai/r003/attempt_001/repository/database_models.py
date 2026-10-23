def normalize_response(response):
    if isinstance(response, dict):
        return {k: normalize_response(v) for k, v in response.items()}
    elif isinstance(response, list):
        return [normalize_response(item) for item in response]
    return response