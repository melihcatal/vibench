def normalize_response(response):
    return {"text": response.document.text, "layout": response.document.pages, "tables": response.document.tables, "key_values": response.document.entities}