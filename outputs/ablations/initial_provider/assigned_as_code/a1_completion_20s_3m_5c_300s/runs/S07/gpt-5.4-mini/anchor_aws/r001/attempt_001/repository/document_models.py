def normalize_text(text):
    if not text:
        return ""
    if isinstance(text, list):
        text = "\n".join(str(part) for part in text if part is not None)
    return str(text).strip()


def normalize_document_bytes(payload):
    if isinstance(payload, dict):
        if "document_bytes" in payload:
            return payload["document_bytes"]
        if "bytes" in payload:
            return payload["bytes"]
    return payload


def normalize_blocks(blocks):
    normalized = []
    for block in blocks or []:
        normalized.append({k.lower(): v for k, v in block.items()})
    return normalized


def extract_lines_from_blocks(blocks):
    return [block.get("text", "") for block in blocks if block.get("blocktype") == "LINE" and block.get("text")]


def extract_kv_from_blocks(blocks):
    items = []
    for block in blocks or []:
        if block.get("blocktype") == "KEY_VALUE_SET":
            items.append(block)
    return items
