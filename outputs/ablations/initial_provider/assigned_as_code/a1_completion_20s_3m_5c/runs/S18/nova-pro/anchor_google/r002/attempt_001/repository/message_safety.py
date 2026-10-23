import re


def check_message_safety(message: str) -> bool:
    unsafe_patterns = [
        r'<script>',
        r'<iframe>',
        r'<object>',
        r'<embed>',
        r'<applet>'
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, message):
            return False
    return True