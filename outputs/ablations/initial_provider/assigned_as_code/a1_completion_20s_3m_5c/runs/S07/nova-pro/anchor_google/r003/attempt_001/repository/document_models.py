def normalize_response(response):
    normalized_response = {}
    if 'text' in response:
        normalized_response['text'] = response['text']
    if 'layout' in response:
        normalized_response['layout'] = response['layout']
    if 'tables' in response:
        normalized_response['tables'] = response['tables']
    if 'key_values' in response:
        normalized_response['key_values'] = response['key_values']
    return normalized_response