def normalize_text(text):
    if not text:
        return ""
    return " ".join(str(text).split())


def normalize_document_text(response):
    return {"text": normalize_text(response.get("text", ""))}


def normalize_key_values(pairs):
    normalized = []
    for item in pairs or []:
        normalized.append({"key": normalize_text(item.get("key", "")), "value": normalize_text(item.get("value", ""))})
    return {"key_values": normalized}


def normalize_sections(sections):
    normalized = []
    for item in sections or []:
        normalized.append({"section": normalize_text(item.get("section", "")), "text": normalize_text(item.get("text", ""))})
    return {"sections": normalized}
