def document_payload(document_bytes, mime_type):
    return {'document_bytes': document_bytes, 'mime_type': mime_type}


def normalize_words(words):
    return [{'text': getattr(word, 'content', ''), 'confidence': getattr(word, 'confidence', None)} for word in words or []]


def normalize_value_pairs(pairs):
    items = []
    for pair in pairs or []:
        items.append({'key': getattr(getattr(pair, 'key', None), 'content', None), 'value': getattr(getattr(pair, 'value', None), 'content', None)})
    return items
