def field_content(field):
    if field is None:
        return None
    return getattr(field, "content", None) or getattr(field, "value_string", None) or getattr(field, "value", None)


def field_confidence(field):
    if field is None:
        return None
    return getattr(field, "confidence", None)


def normalize_line_item(values, keys):
    item = {}
    for output_key, input_key in keys.items():
        item[output_key] = field_content(values.get(input_key))
    return item


def ensure_list(value):
    return value if isinstance(value, list) else []
