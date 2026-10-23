def normalize_document(document):
    return {k: v for k, v in document.items() if v is not None}

def parse_response(response):
    return response.get('Item', None)