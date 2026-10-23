def normalize_labels(labels):
    return [{'name': item.get('name', ''), 'confidence': float(item.get('confidence', 0.0))} for item in labels or []]


def normalize_text_lines(lines):
    return [{'text': item.get('text', ''), 'confidence': float(item.get('confidence', 0.0))} for item in lines or []]


def normalize_safety(categories):
    return [{'name': item.get('name', ''), 'score': float(item.get('score', 0.0))} for item in categories or []]
