def normalize_response(response):
    normalized_response = {}
    for page in response.document.pages:
        normalized_page = {}
        for element in page.layout:
            if element.type_ == 1:  # LAYOUT_TEXT
                normalized_page['text'] = element.text
            elif element.type_ == 2:  # LAYOUT_TABLE
                normalized_page['table'] = element.table
        normalized_response['pages'].append(normalized_page)
    return normalized_response
