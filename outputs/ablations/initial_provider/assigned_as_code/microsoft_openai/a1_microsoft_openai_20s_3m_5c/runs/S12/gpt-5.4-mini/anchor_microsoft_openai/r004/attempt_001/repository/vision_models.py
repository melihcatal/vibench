def normalize_confidence(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def normalize_items(items, name_key='name', confidence_key='confidence'):
    normalized = []
    for item in items or []:
        if isinstance(item, dict):
            name = item.get(name_key) or item.get('text') or item.get('label') or item.get('value')
            confidence = normalize_confidence(item.get(confidence_key, item.get('score', 0.0)))
        else:
            name = getattr(item, name_key, None) or getattr(item, 'text', None) or getattr(item, 'label', None) or getattr(item, 'value', None)
            confidence = normalize_confidence(getattr(item, confidence_key, getattr(item, 'score', 0.0)))
        if name is not None:
            normalized.append({'name': str(name), 'confidence': confidence})
    return normalized
