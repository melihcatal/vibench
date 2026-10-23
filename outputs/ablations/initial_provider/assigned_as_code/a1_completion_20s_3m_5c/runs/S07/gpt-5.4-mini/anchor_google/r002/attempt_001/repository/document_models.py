def normalize_text(text):
    return " ".join((text or "").split())


def normalize_blocks(blocks):
    return [{"text": normalize_text(block.get("text")), "type": block.get("type"), "confidence": block.get("confidence")} for block in blocks or []]


def normalize_tables(tables):
    normalized = []
    for table in tables or []:
        normalized.append({
            "header_rows": table.get("header_rows", []),
            "body_rows": table.get("body_rows", []),
        })
    return normalized


def normalize_key_values(pairs):
    return [{"key": normalize_text(item.get("key")), "value": normalize_text(item.get("value"))} for item in pairs or []]
