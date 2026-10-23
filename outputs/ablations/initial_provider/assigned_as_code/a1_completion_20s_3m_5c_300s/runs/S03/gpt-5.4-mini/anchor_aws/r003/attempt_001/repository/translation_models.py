def normalize_language_code(value):
    if value is None:
        return None
    return str(value).strip()


def normalize_text(value):
    if value is None:
        return ""
    return str(value)


def normalize_payload(payload):
    payload = dict(payload or {})
    return {
        "text": normalize_text(payload.get("text")),
        "source_language": normalize_language_code(payload.get("source_language")),
        "target_language": normalize_language_code(payload.get("target_language")),
    }


def normalize_text_list(payload):
    payload = dict(payload or {})
    return {
        "texts": [normalize_text(item) for item in payload.get("texts", [])],
        "source_language": normalize_language_code(payload.get("source_language")),
        "target_language": normalize_language_code(payload.get("target_language")),
    }


def normalize_markup_payload(payload):
    payload = dict(payload or {})
    return {
        "markup": normalize_text(payload.get("markup")),
        "source_language": normalize_language_code(payload.get("source_language")),
        "target_language": normalize_language_code(payload.get("target_language")),
    }


def normalize_dictionary_payload(payload):
    payload = dict(payload or {})
    return {
        "values": dict(payload.get("values", {})),
        "source_language": normalize_language_code(payload.get("source_language")),
        "target_language": normalize_language_code(payload.get("target_language")),
    }
