def normalize_document_response(response):
    normalized_response = {
        'document_type': response.get('document_type', ''),
        'fields': {}
    }
    for field, value in response.get('fields', {}).items():
        normalized_response['fields'][field] = value.content
    return normalized_response