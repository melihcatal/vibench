import html


def normalize_text_payload(payload):
    if isinstance(payload, str):
        return {
            "text": payload,
            "source_language": None,
            "target_language": None,
        }
    return {
        "text": payload.get("text", ""),
        "source_language": payload.get("source_language"),
        "target_language": payload.get("target_language"),
    }


def normalize_batch_payload(payload):
    data = payload if isinstance(payload, dict) else {"texts": payload}
    return {
        "texts": list(data.get("texts", [])),
        "source_language": data.get("source_language"),
        "target_language": data.get("target_language"),
    }


def normalize_markup_payload(payload):
    data = payload if isinstance(payload, dict) else {"markup": payload}
    return {
        "markup": data.get("markup", ""),
        "source_language": data.get("source_language"),
        "target_language": data.get("target_language"),
    }


def normalize_dictionary_payload(payload):
    data = payload if isinstance(payload, dict) else {"values": payload}
    return {
        "values": dict(data.get("values", {})),
        "source_language": data.get("source_language"),
        "target_language": data.get("target_language"),
    }


def normalize_result(text, source_language, target_language):
    return {
        "text": text,
        "source_language": source_language,
        "target_language": target_language,
    }


def escape_markup_text(text):
    return html.escape(text, quote=False)
