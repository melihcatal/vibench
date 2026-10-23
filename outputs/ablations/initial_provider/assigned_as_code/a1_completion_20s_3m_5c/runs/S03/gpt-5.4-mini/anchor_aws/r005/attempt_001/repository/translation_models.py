import html


def normalize_language_code(value):
    if value is None:
        return None
    return str(value).strip().replace("_", "-").lower()


def normalize_text(value):
    if value is None:
        return ""
    return str(value)


def normalize_segments(value):
    if value is None:
        return []
    return [normalize_text(item) for item in value]


def normalize_dictionary_values(value):
    if value is None:
        return {}
    return {str(key): normalize_text(item) for key, item in value.items()}


def escape_markup_text(value):
    return html.escape(normalize_text(value), quote=False)
