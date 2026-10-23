import re

def check_unsafe_content(payload):
    unsafe_patterns = [
        r'<script>',
        r'<iframe>',
        r'javascript:',
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, payload):
            return True
    return False