def normalize_response(response):
    return response.get('results', [])[0].get('outputText', '')