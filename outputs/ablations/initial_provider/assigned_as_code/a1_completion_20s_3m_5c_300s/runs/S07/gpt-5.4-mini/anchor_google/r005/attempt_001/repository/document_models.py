def normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()


def normalize_key_value_pairs(items):
    pairs = []
    for item in items or []:
        if isinstance(item, dict):
            key = normalize_text(item.get("key"))
            value = normalize_text(item.get("value"))
        else:
            key = normalize_text(getattr(item, "key", None))
            value = normalize_text(getattr(item, "value", None))
        if key or value:
            pairs.append({"key": key, "value": value})
    return pairs


def normalize_layout_blocks(blocks):
    normalized = []
    for block in blocks or []:
        if isinstance(block, dict):
            normalized.append({k: block.get(k) for k in block})
        else:
            normalized.append({"text": normalize_text(getattr(block, "text", None))})
    return normalized
