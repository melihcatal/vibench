import re


def check_unsafe_content(text):
    unsafe_patterns = [r"<script>", r"<iframe>"]
    for pattern in unsafe_patterns:
        if re.search(pattern, text):
            return True
    return False
