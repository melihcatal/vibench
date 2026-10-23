import os

# General helpers that normalize raw SDK responses to a consistent local shape
def normalize_labels(raw_labels):
    return [
        {
            "name": item.get('Name') or item.get('label') or '',
            "confidence": item.get('Confidence') or item.get('score') or 0.0
        }
        for item in raw_labels
    ]

def normalize_description(raw_desc):
    # Azure Vision returns list of captions; take the most confident one
    if isinstance(raw_desc, list):
        return (raw_desc[0].get('text') or '').strip() if raw_desc else ''
    return str(raw_desc).strip()

def normalize_text_detections(raw_lines):
    # Google Vision returns a list of TextAnnotation dicts
    return [
        {
            "text": item.get('description') or item.get('text') or '',
            "confidence": item.get('confidence') or 0.0
        }
        for item in raw_lines
    ]

def normalize_safety(raw_moderation):
    return [
        {
            "name": item.get('Name') or item.get('label') or '',
            "confidence": item.get('Confidence') or item.get('score') or 0.0
        }
        for item in raw_moderation
    ]
