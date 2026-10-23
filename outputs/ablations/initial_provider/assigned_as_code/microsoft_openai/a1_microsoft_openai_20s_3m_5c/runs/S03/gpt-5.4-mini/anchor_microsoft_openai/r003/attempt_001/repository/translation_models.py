def normalize_text(text):
    if text is None:
        return ""
    return str(text)


def normalize_text_list(values):
    return [normalize_text(value) for value in values]


def normalize_dictionary_values(data):
    return {key: normalize_text(value) for key, value in data.items()}


def translation_payload(text, source_language, target_language):
    return {"text": normalize_text(text), "source_language": source_language, "target_language": target_language}
