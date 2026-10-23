import re


def check_unsafe_content(fields):
    unsafe_patterns = [
        r'<script.*?>.*?</script>',
        r'<.*?javascript:.*?>',
        r'<.*?vbscript:.*?>'
    ]
    for field in fields:
        for pattern in unsafe_patterns:
            if re.search(pattern, field):
                return True
    return False