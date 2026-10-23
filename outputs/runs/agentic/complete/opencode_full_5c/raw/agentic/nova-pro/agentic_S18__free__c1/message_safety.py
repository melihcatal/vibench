import re


def message_safety(message):
    unsafe_patterns = [r"<script>", r"<iframe>", r"<object>"]
    for pattern in unsafe_patterns:
        if re.search(pattern, message):
            return False
    return True
