def normalize_thresholds(thresholds=None):
    thresholds = dict(thresholds or {})
    return {str(key): float(value) for key, value in thresholds.items()}


def build_message_result(text, decision, score, categories=None):
    result = {'text': text, 'decision': decision, 'score': score}
    if categories is not None:
        result['categories'] = categories
    return result


def extract_redactions(response):
    items = []
    for item in getattr(response, 'categories_analysis', []) or []:
        category = getattr(item, 'category', None)
        severity = getattr(item, 'severity', 0)
        if severity >= 4:
            items.append({'category': str(category), 'severity': severity})
    return items
