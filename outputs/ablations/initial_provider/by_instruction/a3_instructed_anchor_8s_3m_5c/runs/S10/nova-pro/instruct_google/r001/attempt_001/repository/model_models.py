def normalize_response(response):
    return response.predictions[0]

def format_request(text, parameters=None):
    if parameters is None:
        parameters = {}
    return [text], parameters