def normalize_response(response):
    return response.get('choices', [{}])[0].get('text', '').strip()