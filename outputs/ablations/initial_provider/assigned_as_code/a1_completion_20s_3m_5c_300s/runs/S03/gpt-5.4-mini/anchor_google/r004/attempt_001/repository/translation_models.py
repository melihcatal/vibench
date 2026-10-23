def batch_translate_payload(payload):
    return [{"text": text, "index": index} for index, text in enumerate(payload["texts"])]


def batch_translate_result(translations, items, payload):
    return {
        "texts": [translation.translated_text for translation in translations],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
        "order": [item["index"] for item in items],
    }


def markup_translate_payload(payload):
    return {"text": payload["text"], "mime_type": payload.get("mime_type", "text/html")}


def markup_translate_result(text, payload, normalized):
    return {
        "text": text,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
        "mime_type": normalized["mime_type"],
    }


def dictionary_translate_payload(payload):
    return list(payload["values"].items())


def dictionary_translate_result(payload, normalized, translations):
    return {
        "values": {key: translation.translated_text for (key, _), translation in zip(normalized, translations)},
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
