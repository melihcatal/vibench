def get_document_template(document_id, data):
    return {"id": document_id, "document": data}

def get_document_query_template(field, value):
    return {"field": field, "value": value}

def get_conditional_update_template(document_id, field, value, condition_field, condition_value):
    return {"id": document_id, "field": field, "value": value, "condition_field": condition_field, "condition_value": condition_value}
