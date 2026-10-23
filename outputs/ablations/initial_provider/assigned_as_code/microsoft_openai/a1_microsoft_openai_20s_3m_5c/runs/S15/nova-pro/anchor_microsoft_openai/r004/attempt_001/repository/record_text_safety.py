import re


def check_text_safety(text):
    unsafe_patterns = [
        r'<script>',
        r'<iframe>',
        r'<object>',
        r'<embed>',
        r'<applet>',
        r'<link rel="stylesheet">',
        r'<style>',
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True