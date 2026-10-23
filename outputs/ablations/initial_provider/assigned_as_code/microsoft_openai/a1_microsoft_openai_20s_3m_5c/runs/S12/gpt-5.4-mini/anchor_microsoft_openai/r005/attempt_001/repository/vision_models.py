def normalize_labels(tags, limit):
    return [{'name': tag.name, 'confidence': tag.confidence} for tag in sorted(tags, key=lambda item: item.confidence, reverse=True)[:limit]]


def normalize_text_lines(lines, limit):
    return [{'text': line.text, 'confidence': getattr(line, 'confidence', None)} for line in lines[:limit]]


def normalize_caption(text, confidence=None):
    data = {'caption': text}
    if confidence is not None:
        data['confidence'] = confidence
    return data


def normalize_safety_result(is_safe, categories=None):
    return {'safe': bool(is_safe), 'categories': categories or []}
