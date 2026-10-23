def image_summary(payload, config=None):
    labels = payload.get('labels', [])
    description = payload.get('description', {}).get('text', '')
    text = payload.get('text', [])
    parts = []
    if description:
        parts.append(description)
    if labels:
        parts.append(', '.join(item.get('name', '') for item in labels[:3] if item.get('name')))
    if text:
        parts.append('Text: ' + '; '.join(item.get('text', '') for item in text[:2] if item.get('text')))
    return {'summary': ' | '.join(parts)}
