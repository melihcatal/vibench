def normalize_response(response):
    texts = response.full_text_annotation.text
    normalized_response = {
        'texts': texts,
        'pages': response.full_text_annotation.pages
    }
    return normalized_response