def normalize_text(text):
    return {"text": text or ""}


def normalize_layout(document):
    blocks = []
    for page in getattr(document, "pages", []):
        for block in getattr(page, "blocks", []):
            blocks.append(getattr(block.layout, "text_anchor", None))
    return {"blocks": blocks}


def normalize_tables(document):
    tables = []
    for page in getattr(document, "pages", []):
        for table in getattr(page, "tables", []):
            tables.append({"header_rows": len(getattr(table, "header_rows", [])), "body_rows": len(getattr(table, "body_rows", []))})
    return {"tables": tables}


def normalize_key_values(document):
    pairs = []
    for page in getattr(document, "pages", []):
        for field in getattr(page, "form_fields", []):
            pairs.append({
                "field_name": getattr(getattr(field, "field_name", None), "text_anchor", None),
                "field_value": getattr(getattr(field, "field_value", None), "text_anchor", None),
            })
    return {"key_values": pairs}
