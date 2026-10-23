import re
from google.cloud import dlp_v2


_UNSAFE_PATTERNS = [re.compile(p, re.I) for p in [r'\bpassword\b', r'\bssn\b', r'credit card', r'\bapi[_ -]?key\b']]


def unsafe_copy_check(text, project_id=None):
    findings = []
    for pattern in _UNSAFE_PATTERNS:
        if pattern.search(text):
            findings.append(pattern.pattern)
    client = dlp_v2.DlpServiceClient()
    if project_id:
        parent = f'projects/{project_id}'
        content_item = {'value': text}
        _ = client.inspect_content(request={'parent': parent, 'item': content_item})
    return {'unsafe': bool(findings), 'findings': findings}
