import re


_unsafe_patterns = [re.compile(p, re.IGNORECASE) for p in (r'<script', r'javascript:', r'onerror\s*=', r'onload\s*=')]


def metric_annotation_safety(payload, config=None):
    text = payload.get('text') or payload.get('annotation') or ''
    unsafe = any(pattern.search(text) for pattern in _unsafe_patterns)
    return {'safe': not unsafe, 'reason': None if not unsafe else 'unsafe_annotation_text'}
