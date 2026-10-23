def normalize_document_response(response):
    fields, items = {}, []
    for entity in response.document.entities:
        if entity.type_ == "line_item":
            values = {p.type_.split("/")[-1]: p.mention_text for p in entity.properties}
            items.append({"description": values.get("description"), "quantity": values.get("quantity"), "amount": values.get("amount")})
        else:
            fields[entity.type_] = entity.mention_text
    return fields, items