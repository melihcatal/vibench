def normalize_response(response):
    return [pred['outputs'][0]['embedding'] for pred in response.predictions]