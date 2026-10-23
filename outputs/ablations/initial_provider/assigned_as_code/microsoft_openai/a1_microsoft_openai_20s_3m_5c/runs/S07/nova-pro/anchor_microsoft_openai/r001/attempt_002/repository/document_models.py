def normalize_text_response(response):
    return {'text': response.content}

def normalize_layout_response(response):
    return {'layout': response.content}

def normalize_tables_response(response):
    return {'tables': response.content}

def normalize_key_values_response(response):
    return {'key_values': response.content}