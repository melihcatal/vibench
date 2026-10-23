def normalize_document_text(text):
    return " ".join((text or "").split())


def normalize_blocks(blocks):
    items = []
    for block in blocks or []:
        items.append(
            {
                "type": getattr(block, "type_", None),
                "text": normalize_document_text(getattr(block, "layout", None).text_anchor.content if getattr(block, "layout", None) and getattr(getattr(block, "layout", None), "text_anchor", None) and hasattr(getattr(getattr(block, "layout", None), "text_anchor", None), "content") else ""),
            }
        )
    return items


def normalize_key_value_pairs(doc):
    pairs = []
    for entity in getattr(doc, "entities", []) or []:
        pairs.append({"key": getattr(entity, "type_", None), "value": getattr(entity, "mention_text", None)})
    return pairs
